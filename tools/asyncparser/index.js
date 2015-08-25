var https = require('https');
var htmlparser = require("htmlparser2");

var categoryId = 0;
var subCategoryId = 0;
var subCategoryListId = 0;
var subCategoryItemId = 0;

var CategoryLink = function (url, description, main_cat, sub_cat, sub_sub_cat) {
  // define category keys
  this.categoryId = categoryId;
  this.subCategoryId = (main_cat)? subCategoryId : null;
  this.subCategoryListId = (sub_cat)? subCategoryListId : null;
  this.subCategoryItemId = (sub_sub_cat)? subCategoryItemId : null;
  this.url = url;
  this.description = description;
};

// Catalog parser
var inCatalog = false;
var inSubCatalog = false;
var inSubCatalogList = false;
var inSubCatalogItem = false;
var catalogLevel = 0;
var subCatalogLevel = 0;
var subCatalogListLevel = 0;
var subCatalogItemLevel = 0;

var thisIsLink = false;
var links = [];

var href = '';
var parserStructure = new htmlparser.Parser({
  onopentag: function(name, attribs) {
    if (name === 'li' && attribs.class === 'item __submenu') {
      inCatalog = true;
    }
    if (name === 'div' && attribs.class === 'subcatalog') {
      inSubCatalog = true;
    }
    if (name === 'div' && attribs.class === 'subcatalog_list') {
      inSubCatalogList = true;
    }
    if (name === 'li' && attribs.class === 'subcatalog_item ') {
      inSubCatalogItem = true;
    }
    if (inCatalog) catalogLevel++;
    if (inSubCatalog) subCatalogLevel++;
    if (inSubCatalogList) subCatalogListLevel++;
    if (inSubCatalogItem) subCatalogItemLevel++;
    if ((inCatalog || inSubCatalog) && (name === 'a')) {
      if (attribs.href.substr(0, 9) === '/category') {
        thisIsLink = true;
        href = attribs.href;
      }
    }
  },
  ontext: function(text) {
    if (thisIsLink) {
      links.push(new CategoryLink(href, text, inCatalog, inSubCatalogList, inSubCatalogItem));
      thisIsLink = false;
    }
  },
  onclosetag: function(name) {
    if (inCatalog && catalogLevel > 0) catalogLevel--;
    if (inCatalog && catalogLevel == 0) {
      inCatalog = false;
      categoryId++;
    }
    if (inSubCatalog && subCatalogLevel > 0) subCatalogLevel--;
    if (inSubCatalog && subCatalogLevel == 0) {
      inSubCatalog = false;
      subCategoryId++;
    }
    if (inSubCatalogList && subCatalogListLevel > 0) subCatalogListLevel--;
    if (inSubCatalogList && subCatalogListLevel == 0) {
      inSubCatalogList = false;
      subCategoryListId++;
    }
    if (inSubCatalogItem && subCatalogItemLevel > 0) subCatalogItemLevel--;
    if (inSubCatalogItem && subCatalogItemLevel == 0) {
      inSubCatalogItem = false;
      subCategoryItemId++;
    }
  }
}, {decodeEntities: true});

var catalogItemId = 0;
// Items parser
var SubCatalogParserEmitter = function(link) {
  this.categoryId = '\t"main_cat": ' + link.subCategoryId + ',\n' + 
                    '\t"sub_cat": ' + link.subCategoryListId + ',\n' +
                    '\t"sub_sub_cat": ' + link.subCategoryItemId + ',\n';
  this.inItem = false;
  this.deepLevel = 0;
  this.inTitle = false;
}

SubCatalogParserEmitter.prototype.onopentag = function(tagname, attributes) {
  // is it item div
  if (tagname === 'div' && attributes.class === 'catalog-i') {
    this.inItem = true;
    process.stdout.write('{\n' + this.categoryId);
  }
  if (this.inItem) {
    this.deepLevel++;
    if (tagname === 'div' && attributes.class === 'catalog-i_title') this.inTitle = true;
    if (tagname === 'div' && attributes.class === 'item-price') this.inPrice = true;

    if (tagname === 'a' && attributes.class === 'add-to-list') {
      process.stdout.write('\t"article" : ' + attributes["data-article"] + ',\n');
      process.stdout.write('\t"box_size" : ' + attributes["data-box_size"] + ',\n');
      process.stdout.write('\t"act_price" : ' + attributes["data-act_price"] + ',\n');
      process.stdout.write('\t"regular_price" : ' + attributes["data-regular_price"] + ',\n');
      process.stdout.write('\t"isstockempty" : ' + attributes["data-isstockempty"] + '\n');
    }
    if (tagname === 'a' && attributes.class === 'catalog-i_link') {
      process.stdout.write('\t"detailed_link": "' + attributes.href + '",\n');
    }
    // parse img source
    if (tagname === "img" && this.inItem) {
      process.stdout.write('\t"img_url": "' + attributes.src + '",\n');
    }
  }
}

SubCatalogParserEmitter.prototype.ontext = function(text) {
  // parse text from item card
  text = text.trim();
  if (this.inItem && text.length > 1) {
    if (this.inTitle) process.stdout.write('\t"title": "' + text + '",\n');
  }
}

SubCatalogParserEmitter.prototype.onclosetag = function(tagname) {
  // calculate closing divs
  if (this.inTitle) this.inTitle = false;
  if (this.inIntPrice) this.inIntPrice = false;
  if (this.inFloatPrice) this.inFloatPrice = false;

  if (this.inItem && this.deepLevel > 0) this.deepLevel--;
  if (this.inItem && this.deepLevel == 0) {
    process.stdout.write("},\n");
    this.inItem = false;
    catalogItemId++;
  }
}


var parseStructure = function () {
  // options for request main page with structure
  var optionsStructure = {
    hostname: 'kazan.metro-cc.ru',
    port: 443,
    method: 'GET'
  };

  var reqStructure = https.request(optionsStructure, function(res) {
    res.on('data', function(data) {
      parserStructure.write(data);
    });
    res.on('end', function() {
      process.stdout.write('"categories": [\n');
      for (var i = 0, len = links.length; i < len; i++) {
        process.stdout.write('{\n' + 
          '\t"main_cat": ' + links[i].categoryId + ',\n' +
          '\t"sub_cat": ' + links[i].subCategoryListId + ',\n' +
          '\t"sub_sub_cat": ' + links[i].subCategoryItemId + ',\n' +
          '\t"name": "' + links[i].description + '"\n}');
        if (i+1<len) process.stdout.write(',\n');
      }
      process.stdout.write('\n],\n');
      parserStructure.end();
      process.stdout.write('\n"products": [\n');
      parseCatalogs(links);
    });
  });
  reqStructure.end();
}

var parseSubCatalog = function(link) {
  // options for example request
  var parserSubCatalog = new htmlparser.Parser(new SubCatalogParserEmitter(link), {decodeEntities: true});

  var options = {
    hostname: 'kazan.metro-cc.ru',
    port: 443,
    path: link.url + '?limit=10000',
    method: 'GET'
  };

  var req = https.request(options, function(res) {
    res.on('data', function(data) {
      parserSubCatalog.write(data);
    });
    res.on('end', function() {
      parserSubCatalog.end();
      // process.stdout.write('\n**parse time ' + process.uptime());
    });
  });
  req.end();
}

var parseCatalogs = function(links) {
  for (var i = 0, len = links.length; i < len; i++) {
    if ((links[i].url) && (links[i].url.substr(0, 9) === '/category')) {
      parseSubCatalog(links[i]);
    }
  }
}

parseStructure();