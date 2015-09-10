var actions = Reflux.createActions([
    'addToBasket', 'decFromBasket'
]);

var ProductStore = Reflux.createStore({
    init: function() {
        this.data = [];
    },
    setInitialState: function(products) {
        this.data = products;
    },
    getInitialState: function() {
        return this.data;
    },
    getProduct: function(id) {
        return this.data[id];
    },
    add: function( product ) {
        this.data[product.id] = product;
    }
});

var BasketStore = Reflux.createStore({
    init: function() {
        this.data = [];
        this.listenTo(actions.addToBasket, this.onAddToBasket);
        this.listenTo(actions.decFromBasket, this.onDecFromBasket);
    },
    initialize: function(url, get_url){
        this.url = url;
        var self = this;
        $.get(get_url, function(res){
            res = JSON.parse(res);
            for(var i in res) {
                ProductStore.add(res[i].product);
                self.data[res[i].product.id] = res[i];
            }
            self.trigger( self.totalSum() );
        })
    },
    onDecFromBasket: function(id, remove){
        if( this.data[id] ) {
            var cnt = remove ? this.data[id].count : 1;
            this.data[id].count = this.data[id].count - cnt;
            if( this.data[id].count <= 0 )
                delete this.data[id];
            $.get( this.url + '?id=' + id + '&count=-' + cnt, function(res){  } );
            this.trigger( this.totalSum() );
        }
    },
    onAddToBasket: function(id) {
        if( this.data[id] ) {
            this.data[id].count = this.data[id].count + 1;
        }
        else {
            var product = ProductStore.getProduct(id);
            if( product ) this.data[id] = { count: 1, product: product};
        }
        $.get( this.url + '?id=' + id + '&count=1', function(res){  } );
        this.trigger( this.totalSum() );
    },
    totalSum: function() {
        var total = 0;
        for(var i in this.data)
            total += this.data[i].count * this.data[i].product.price;
        return total;
    },
    getInitialState: function() {
        return this.data;
    },
    get: function(id){
        return this.data[id];
    },
    items: function() {
        return this.data;
    },
    getProductCount: function(id) {
        return this.data[id] ? this.data[id].count : 0;
    }
});

var Price = React.createClass({
    mixins: [Reflux.listenTo(BasketStore, "onBasketChange")],
    onBasketChange: function(total) {
        this.setProps({ count: BasketStore.getProductCount(this.props.id) });
    },
    onClick: function() {
        actions.addToBasket(this.props.id);
    },
    render: function() {
        var button_class = "btn btn-xs product__add ";
        button_class += this.props.count > 0 ? "btn-info" : "btn-default";
        var cnt = this.props.count > 0 ? ' [' + this.props.count + ']'  : '';
        return (
            <div className={button_class} onClick={this.onClick}>
                <span className="product__price">
                    <i className="fa fa-cart-plus"></i> { this.props.price }</span> <i className="fa fa-ruble"></i>
                    {cnt}
            </div>
        );
    }
});

var Basket = React.createClass({
    mixins: [Reflux.listenTo(BasketStore, "onBasketChange")],
    onBasketChange: function(total) {
        this.setProps({ price: total });
    },
    render: function() {
        var has_price = this.props.price > 0;
        var basket_class = "label label" + (has_price ? '-success' : '-default');
        var price = has_price ? <span className="basket__price"> {this.props.price} <i className="fa fa-ruble"></i></span> : '';
        return (
                <a href={this.props.url} className="basket">
                    <span className={basket_class}>
                        <i className="fa fa-shopping-cart"></i> Корзина
                        { price }
                    </span>
                </a>
        );
    }
});

var BasketLine = React.createClass({
    add: function() {
        actions.addToBasket(this.props.product.id);
    },
    dec: function() {
        actions.decFromBasket(this.props.product.id);
    },
    remove: function() {
        actions.decFromBasket(this.props.product.id, true);
    },
    render: function() {
        var sum = this.props.product.price * this.props.count;
        return (<tr className="basket-list__line">
                    <td>
                        <div className="btn btn-xs btn-default" onClick={this.add}><i className="fa fa-plus"></i></div>
                        <div className="btn btn-xs btn-default" onClick={this.dec}><i className="fa fa-minus"></i></div>
                        <div className="btn btn-xs btn-default" onClick={this.remove}><i className="fa fa-remove"></i></div>
                        &nbsp;
                        <span className="badge">{this.props.product.price} * {this.props.count} = {sum}<i className="fa fa-ruble" /></span>
                    </td>
                    <td>
                        <span dangerouslySetInnerHTML={{__html: this.props.product.name}} />
                    </td>
                </tr>
            )
    }
});

var BasketList = React.createClass({
    mixins: [Reflux.listenTo(BasketStore, "onBasketChange")],
    onBasketChange: function(total) {
        this.setProps({ items: BasketStore.items(), total: BasketStore.totalSum() });
    },
    render: function() {
        var self = this;
        var items = this.props.items;
        var list = items ?
            items.map( function( item ){ item.key = item.product.id; return (<BasketLine {...item} />); })
            : '';
        var btn = this.props.link ?
                    (<a className="btn btn-info" href={this.props.link} alt="Перейти в корзину">
                        <i className="fa fa-shopping-cart" /> { this.props.total } <i className="fa fa-ruble" />
                    </a>)
                    : (<div>Итого: { this.props.total } <i className="fa fa-ruble"></i></div>);
        return this.props.total > 0 ? (
           <div className="basket-list">
                <div className="panel panel-default">
                  <div className="panel-heading">{ btn }</div>
                  <div className="panel-body">
                    <table><tbody>{list}</tbody></table>
                  </div>
                </div>
           </div>
        ) : (<div />);
    }
});
