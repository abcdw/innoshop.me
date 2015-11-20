var actions = Reflux.createActions([
    'addToBasket', 'decFromBasket', 'clearBusket', 'updateLogin'
]);

var Store = function (key) {
    var self = this;

    this.key = key;
    this.storage = window.localStorage;
    this.onUpdatedCallback = undefined;

    if (window.localStorage) {
        $(window).on('storage', function (event) {
            if (self.onUpdatedCallback && event.originalEvent.key == self.key) {
                var data = event.originalEvent.newValue || false;
                data = JSON.parse(data);
                self.onUpdatedCallback(data);
            }
        });
    }

    this.onUpdated = function (callback) {
        this.onUpdatedCallback = callback;
    };

    this.get = function () {
        if (!self._check())
            return false;
        var data = self.storage.getItem(self.key);
        data = data || false;
        data = JSON.parse(data);
        return data;
    };

    this.set = function (data) {
        if (!self._check())
            return false;
        data = data || false;
        self.storage.setItem(self.key, JSON.stringify(data));
    };

    this._check = function () {
        return this.storage != undefined;
    };
};

var ProductStore = Reflux.createStore({
    init: function () {
        this.data = [];
    },
    setInitialState: function (products) {
        this.data = products;
    },
    getInitialState: function () {
        return this.data;
    },
    getProduct: function (id) {
        return this.data[id];
    },
    add: function (product) {
        this.data[product.id] = product;
    }
});

var ClientStore = Reflux.createStore({
    init: function () {
        var self = this;
        this.storage = new Store('client-login-data');

        this.data = this.storage.get() || {login: '', comment: ''};
        this.listenTo(actions.updateLogin, this.onLoginChange);

        this.storage.onUpdated(function (data) {
            var d = data || {login: '', comment: ''};
            self.update(d.login, d.comment, true);
        });
    },
    getInitialState: function () {
        return this.data;
    },
    update: function (login, comment, dontStore) {
        this.data.login = login;
        this.data.comment = comment;
        this.trigger(this.data);
        if (!dontStore)
            this.storage.set(this.data);
    },
    onLoginChange: function (login, comment) {
        this.update(login, comment);
    }
});

var BasketStore = Reflux.createStore({
    init: function () {
        var self = this;
        this.storage = new Store('client-basket-data');
        this.data = [];
        this.listenTo(actions.addToBasket, this.onAddToBasket);
        this.listenTo(actions.decFromBasket, this.onDecFromBasket);
        this.listenTo(actions.clearBusket, this.onClearFromBasket);
        this.storage.onUpdated(function (data) {
            data = data || [];
            var arr = [];
            for (var i in data) {
                if (data.hasOwnProperty(i)) {
                    arr[i] = data[i];
                }
            }
            self.update(arr);
        });
    },
    store: function () {
        this.storage.set($.extend({}, this.data));
    },
    initialize: function (url, get_url) {
        this.url = url;
        var self = this;
        $.get(get_url, function (res) {
            res = JSON.parse(res);
            for (var i in res) {
                ProductStore.add(res[i].product);
                self.data[res[i].product.id] = res[i];
            }
            self.trigger(self.totalSum());
            self.store();
        })
    },
    update: function (data) {
        this.data = [];
        data.forEach(function (product, id) {
            if (id != undefined && product)
                this.data[id] = product;
        }, this);
        this.trigger(this.totalSum());
    },
    onClearFromBasket: function () {
        var self = this;
        for (var i in this.data) {
            this.onDecFromBasket(this.data[i].product.id, true, true);
        }
        this.data = [];
        this.trigger(0);
        this.store();
    },
    onDecFromBasket: function (id, remove, dontStore) {
        if (this.data[id]) {
            var cnt = remove ? this.data[id].count : 1;
            this.data[id].count = this.data[id].count - cnt;
            if (this.data[id].count <= 0)
                delete this.data[id];
            $.get(this.url + '?id=' + id + '&count=-' + cnt, function (res) {
            });
            this.trigger(this.totalSum());
            if (!dontStore)
                this.store();
        }
    },
    onAddToBasket: function (id) {
        if (this.data[id]) {
            this.data[id].count = this.data[id].count + 1;
        }
        else {
            var product = ProductStore.getProduct(id);
            if (product) this.data[id] = {count: 1, product: product};
        }
        $.get(this.url + '?id=' + id + '&count=1', function (res) {
        });
        this.trigger(this.totalSum());
        this.store();
    },
    totalSum: function () {
        var total = 0;
        for (var i in this.data)
            total += this.data[i].count * this.data[i].product.price;
        return total;
    },
    getInitialState: function () {
        return this.data;
    },
    get: function (id) {
        return this.data[id];
    },
    items: function () {
        return this.data;
    },
    getProductCount: function (id) {
        return this.data[id] ? this.data[id].count : 0;
    }
});

var Price = React.createClass({
    mixins: [Reflux.listenTo(BasketStore, "onBasketChange")],
    onBasketChange: function (total) {
        this.setProps({count: BasketStore.getProductCount(this.props.id)});
    },
    onClick: function () {
        actions.addToBasket(this.props.id);
    },
    render: function () {
        var button_class = "btn product__add ";
        button_class += this.props.count > 0 ? "btn-info" : "btn-default";
        var cnt = this.props.count > 0 ? ' [' + this.props.count + ']' : '';
        return (
            <div className={button_class} onClick={this.onClick}>
                <span className="product__price">
                    <i style={ { lineHeight: '8px' } } className="fa fa-plus"></i>&nbsp;&nbsp;в карму</span>
                {cnt}
            </div>
        );
    }
});

var Basket = React.createClass({
    mixins: [Reflux.listenTo(BasketStore, "onBasketChange")],
    onBasketChange: function (total) {
        this.setProps({price: total});
        $(this.getDOMNode()).parent().show();
    },
    onClick: function (event) {
        event.preventDefault();
        $('#basket-list').slideToggle();
    },
    render: function () {
        var has_price = this.props.price > 0;
        var basket_class = "btn btn" + (has_price ? '-success' : '-default');
        var price = has_price ?
            <span className="basket__price"> {this.props.price} <i className="fa fa-ruble"></i></span> : '';
        return (
            <a href={this.props.url} onClick={this.onClick} className="basket">
                    <span className={basket_class}>
                        <i className="fa fa-opencart"></i> Карма
                        { price }
                    </span>
            </a>
        );
    }
});

var BasketLine = React.createClass({
    add: function () {
        actions.addToBasket(this.props.product.id);
    },
    dec: function () {
        actions.decFromBasket(this.props.product.id);
    },
    remove: function () {
        actions.decFromBasket(this.props.product.id, true);
    },
    render: function () {
        var sum = this.props.product.price * this.props.count;
        var min_count = this.props.product.min_count > 1 ? (
            <span className="text-muted"><i className="fa fa-close"></i> {this.props.product.min_count}</span>) : '';
        var price = this.props.product.min_count > 1 ?
            (<span> {this.props.product.min_count}
                x {(this.props.product.price / this.props.product.min_count).toFixed(1)}
                = {this.props.product.price}</span>)
            : (this.props.product.price);
        return (<div className="row basket-list__line">
                <div className="col-xs-2 col-sm-1 col-md-1 col-lg-1 text-right">
                    <div className="btn  btn-default" onClick={this.add}><i className="fa fa-plus"></i></div>
                </div>
                <div className="col-xs-2 col-sm-1 col-md-1 col-lg-1">
                    <div className="btn  btn-default" onClick={this.dec}><i className="fa fa-minus"></i></div>
                </div>
                <div className="h4 col-xs-3 col-sm-2 col-md-2 col-lg-2">
                    {this.props.count}&nbsp;{min_count}
                </div>
                <div className="hidden-xs visible-sm col-sm-6 visible-md col-md-6 visible-lg col-lg-6">
                    <span dangerouslySetInnerHTML={{__html: this.props.product.name}}/>
                    <sup className="text-danger" style={ { whiteSpace: 'nowrap' } }> {price} <i
                        className="fa fa-ruble"></i></sup>
                </div>
                <div className="h4 col-xs-5 col-sm-2 col-md-2 col-lg-2 text-right">
                    {sum}&nbsp;<i className="fa fa-ruble"/>
                </div>
                <div className="col-xs-12 visible-xs hidden-sm hidden-md hidden-lg">
                    <span dangerouslySetInnerHTML={{__html: this.props.product.name}}/>
                    <sup className="text-danger" style={ { whiteSpace: 'nowrap' } }> {price} <i
                        className="fa fa-ruble"></i></sup>
                </div>
            </div>
        )
    }
});

var BasketForm = React.createClass({
    mixins: [Reflux.listenTo(ClientStore, "onLoginChange")],
    onLoginChange: function (data) {
        this.setState(data);
    },
    getInitialState: function () {
        return ClientStore.getInitialState();
    },
    handleChangeLogin: function (event) {
        actions.updateLogin(event.target.value, this.state.comment);
    },
    handleChangeComment: function (event) {
        actions.updateLogin(this.state.login, event.target.value);
    },
    render: function () {
        var login = this.state.login;
        var comment = this.state.comment;
        return (<div><br></br>
            <div className="form-group">
                <input ref="telegram" value={ login } onChange={this.handleChangeLogin}
                       type="text" id="contact" name="contact" className="form-control"
                       placeholder="@telegram или номер телефона"></input>
            </div>
            <div className="form-group">
                    <textarea name="comment" value={ comment } onChange={this.handleChangeComment}
                              id="comment" cols="30" rows="3" placeholder="Комментарий"
                              className="form-control"></textarea>
            </div>
            <div className="form-group">
                <label><input type="checkbox" name="agree_for_analogue" defaultChecked={1} /> Разрешить замену товаров на аналогичные</label>
            </div>
        </div>);
    },
    check: function () {
        var $login = $(this.refs.telegram.getDOMNode()),
            $group = $login.parents('.form-group');
        $group.removeClass("has-error");
        if ($login.val().trim() == '') {
            $group.addClass("has-error");
            $login.focus();
            return false;
        }
        return true;
    }
});

var BasketList = React.createClass({
    mixins: [Reflux.listenTo(BasketStore, "onBasketChange")],
    onBasketChange: function (total) {
        this.setProps({items: BasketStore.items(), total: BasketStore.totalSum()});
    },
    onClose: function () {
        $(this.getDOMNode()).parents('#basket-list').slideToggle();
    },
    clearBusket: function () {
        actions.clearBusket();
    },
    onSubmit: function (event) {
        if (!this.refs.form.check())
            event.preventDefault();
    },
    render: function () {
        var self = this;
        var items = this.props.items;
        var list = items ?
            items.map(function (item) {
                item.key = item.product.id;
                return (<BasketLine {...item} />);
            })
            : '';
        var btn = this.props.link ?
            (<button onClick={ this.onSubmit } type="submit" target="orderForm" className="btn btn-success"
                     href={this.props.link} alt="Потратить карму">
                <i className="fa fa-shopping-cart"/>&nbsp;&nbsp;Потратить
            </button>)
            : '';
        var btn_cear = this.props.items && this.props.items.length > 0 ?
            (<div onClick={this.clearBusket} className="btn btn-danger">
                <i className="fa fa-trash-o"></i>
            </div>) : '';
        var form = this.props.link ? ( <BasketForm ref="form"/> ) : '';
        var karma = this.props.total > 0 ? (<span>{this.props.total} <i className="fa fa-ruble"></i></span>) : 'чиста';
        var csrf = this.props.csrf_token ? (
            <input type="hidden" name="csrfmiddlewaretoken" value={this.props.csrf_token}></input>) : '';
        var header = (<div className="row">
            <span className="h3 col-xs-12 col-sm-8 col-md-9 col-lg-9">Ваша карма { karma }</span>

            <div className="h3 col-xs-12 col-sm-4 col-md-3 col-lg-3 ">
                <div className="btn-group">
                    { btn }
                    { btn_cear }
                    <div onClick={this.onClose} className="btn btn-default">
                        <i className="fa fa-chevron-up"></i>
                    </div>
                </div>
            </div>
        </div>);
        return (items || this.props.link) ? (
            <div className="basket-list">
                <form action={this.props.link} id="orderForm" method="POST">
                    {csrf}
                    <div className="panel panel-default">
                        <div className="panel-heading">
                            { header }
                        </div>
                        <div className="panel-body">
                            {form}
                            <div className="container-fluid">{list}</div>
                        </div>
                        <div className="panel-footer">
                            { header }
                        </div>
                    </div>
                </form>
            </div>
        ) : (<div></div>);
    }
});

var Messages = React.createClass({
    getInitialState: function () {
        return {messages: []};
    },
    componentDidMount: function () {
        var self = this;
        $.get(this.props.link, function (data) {
            self.replaceState({messages: JSON.parse(data)});
        })
    },
    render: function () {
        var msgs = (this.state.messages.map(function (message) {
            return (<div key={message.name} className="panel panel-default">
                <div className="panel-heading">{message.name}</div>
                <div className="panel-body" dangerouslySetInnerHTML={{__html: message._text_rendered}}></div>
            </div>);
        }));
        return (<div>{msgs}</div>);
    }
});

var Rating = React.createClass({
    inc: function (cnt) {
        var self = this;
        $.get(this.props.url + '?id=' + this.props.id + '&count=' + cnt, function (res) {
            console.log(res);
            res = JSON.parse(res);
            if (res.status == 'ok') {
                self.setProps({rating: res.result});
            }
        });
    },
    onInc: function () {
        this.inc(1);
    },
    onDec: function () {
        this.inc(-1);
    },
    render: function () {
        return (<div className="">
            <span className="label label-default"><i className="fa fa-star"></i> { this.props.rating }</span>&nbsp;
            <div className="btn-group">
                <button onClick={this.onInc} className="btn btn-default btn-xs"><i className="fa fa-plus"></i></button>
                <button onClick={this.onDec} className="btn btn-default btn-xs"><i className="fa fa-minus"></i></button>
            </div>
            <br></br>
        </div>);
    }
});