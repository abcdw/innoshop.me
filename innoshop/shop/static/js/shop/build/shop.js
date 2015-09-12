'use strict';

var actions = Reflux.createActions(['addToBasket', 'decFromBasket', 'clearBusket', 'updateLogin']);

var ProductStore = Reflux.createStore({
    init: function init() {
        this.data = [];
    },
    setInitialState: function setInitialState(products) {
        this.data = products;
    },
    getInitialState: function getInitialState() {
        return this.data;
    },
    getProduct: function getProduct(id) {
        return this.data[id];
    },
    add: function add(product) {
        this.data[product.id] = product;
    }
});

var ClientStore = Reflux.createStore({
    init: function init() {
        var self = this;
        this.storage = window.localStorage;
        var data = this.storage.getItem('client-login-data');
        this.data = { login: '', comment: '' };
        if (data) {
            data = JSON.parse(data);
            this.data = data;
        }
        this.listenTo(actions.updateLogin, this.onLoginChange);
        $(window).on('storage', function (event) {
            if (event.originalEvent.key == 'client-login-data') {
                var data = JSON.parse(event.originalEvent.newValue);
                self.update(data.login, data.comment, true);
            }
        });
    },
    getInitialState: function getInitialState() {
        return this.data;
    },
    update: function update(login, comment, dontStore) {
        this.data.login = login;
        this.data.comment = comment;
        this.trigger(this.data);
        if (!dontStore) this.storage.setItem('client-login-data', JSON.stringify(this.data));
    },
    onLoginChange: function onLoginChange(login, comment) {
        this.update(login, comment);
    }
});

var BasketStore = Reflux.createStore({
    init: function init() {
        var self = this;
        this.storage = window.localStorage;
        this.data = [];
        this.listenTo(actions.addToBasket, this.onAddToBasket);
        this.listenTo(actions.decFromBasket, this.onDecFromBasket);
        this.listenTo(actions.clearBusket, this.onClearFromBasket);
        $(window).on('storage', function (event) {
            if (event.originalEvent.key == 'client-basket-data') {
                var data = JSON.parse(event.originalEvent.newValue);
                self.update(data);
            }
        });
    },
    initialize: function initialize(url, get_url) {
        this.url = url;
        var self = this;
        $.get(get_url, function (res) {
            res = JSON.parse(res);
            for (var i in res) {
                ProductStore.add(res[i].product);
                self.data[res[i].product.id] = res[i];
            }
            self.trigger(self.totalSum());
        });
    },
    update: function update(data) {
        this.data = [];
        data.forEach(function (product, id) {
            if (id && product) this.data[id] = product;
        }, this);
        this.trigger(this.totalSum());
    },
    onClearFromBasket: function onClearFromBasket() {
        var self = this;
        for (var i in this.data) {
            this.onDecFromBasket(this.data[i].product.id, true);
        }
        this.data = [];
        this.trigger(0);
        this.storage.setItem('client-basket-data', JSON.stringify(this.data));
    },
    onDecFromBasket: function onDecFromBasket(id, remove) {
        if (this.data[id]) {
            var cnt = remove ? this.data[id].count : 1;
            this.data[id].count = this.data[id].count - cnt;
            if (this.data[id].count <= 0) delete this.data[id];
            $.get(this.url + '?id=' + id + '&count=-' + cnt, function (res) {});
            this.trigger(this.totalSum());
            this.storage.setItem('client-basket-data', JSON.stringify(this.data));
        }
    },
    onAddToBasket: function onAddToBasket(id) {
        if (this.data[id]) {
            this.data[id].count = this.data[id].count + 1;
        } else {
            var product = ProductStore.getProduct(id);
            if (product) this.data[id] = { count: 1, product: product };
        }
        $.get(this.url + '?id=' + id + '&count=1', function (res) {});
        this.trigger(this.totalSum());
        this.storage.setItem('client-basket-data', JSON.stringify(this.data));
    },
    totalSum: function totalSum() {
        var total = 0;
        for (var i in this.data) total += this.data[i].count * this.data[i].product.price;
        return total;
    },
    getInitialState: function getInitialState() {
        return this.data;
    },
    get: function get(id) {
        return this.data[id];
    },
    items: function items() {
        return this.data;
    },
    getProductCount: function getProductCount(id) {
        return this.data[id] ? this.data[id].count : 0;
    }
});

var Price = React.createClass({
    displayName: 'Price',

    mixins: [Reflux.listenTo(BasketStore, "onBasketChange")],
    onBasketChange: function onBasketChange(total) {
        this.setProps({ count: BasketStore.getProductCount(this.props.id) });
    },
    onClick: function onClick() {
        actions.addToBasket(this.props.id);
    },
    render: function render() {
        var button_class = "btn product__add ";
        button_class += this.props.count > 0 ? "btn-info" : "btn-default";
        var cnt = this.props.count > 0 ? ' [' + this.props.count + ']' : '';
        return React.createElement(
            'div',
            { className: button_class, onClick: this.onClick },
            React.createElement(
                'span',
                { className: 'product__price' },
                React.createElement('i', { style: { lineHeight: '8px' }, className: 'fa fa-plus' }),
                '  в карму'
            ),
            cnt
        );
    }
});

var Basket = React.createClass({
    displayName: 'Basket',

    mixins: [Reflux.listenTo(BasketStore, "onBasketChange")],
    onBasketChange: function onBasketChange(total) {
        this.setProps({ price: total });
    },
    onClick: function onClick(event) {
        event.preventDefault();
        $('#basket-list').slideToggle();
    },
    render: function render() {
        var has_price = this.props.price > 0;
        var basket_class = "btn btn" + (has_price ? '-success' : '-default');
        var price = has_price ? React.createElement(
            'span',
            { className: 'basket__price' },
            ' ',
            this.props.price,
            ' ',
            React.createElement('i', { className: 'fa fa-ruble' })
        ) : '';
        return React.createElement(
            'a',
            { href: this.props.url, onClick: this.onClick, className: 'basket' },
            React.createElement(
                'span',
                { className: basket_class },
                React.createElement('i', { className: 'fa fa-opencart' }),
                ' Карма',
                price
            )
        );
    }
});

var BasketLine = React.createClass({
    displayName: 'BasketLine',

    add: function add() {
        actions.addToBasket(this.props.product.id);
    },
    dec: function dec() {
        actions.decFromBasket(this.props.product.id);
    },
    remove: function remove() {
        actions.decFromBasket(this.props.product.id, true);
    },
    render: function render() {
        var sum = this.props.product.price * this.props.count;
        var min_count = this.props.product.min_count > 1 ? React.createElement(
            'sup',
            { className: 'text-info' },
            this.props.product.min_count
        ) : '';
        return React.createElement(
            'div',
            { className: 'row basket-list__line' },
            React.createElement(
                'div',
                { className: 'col-xs-2 col-sm-1 col-md-1 col-lg-1 text-right' },
                React.createElement(
                    'div',
                    { className: 'btn  btn-default', onClick: this.add },
                    React.createElement('i', { className: 'fa fa-plus' })
                )
            ),
            React.createElement(
                'div',
                { className: 'col-xs-2 col-sm-1 col-md-1 col-lg-1' },
                React.createElement(
                    'div',
                    { className: 'btn  btn-default', onClick: this.dec },
                    React.createElement('i', { className: 'fa fa-minus' })
                )
            ),
            React.createElement(
                'div',
                { className: 'h4 col-xs-2 col-sm-1 col-md-1 col-lg-1' },
                this.props.count,
                ' ',
                min_count
            ),
            React.createElement(
                'div',
                { className: 'hidden-xs visible-sm col-sm-8 visible-md col-md-8 visible-lg col-lg-8' },
                React.createElement('span', { dangerouslySetInnerHTML: { __html: this.props.product.name } }),
                React.createElement(
                    'sup',
                    { className: 'text-danger', style: { whiteSpace: 'nowrap' } },
                    ' ',
                    this.props.product.price,
                    ' ',
                    React.createElement('i', { className: 'fa fa-ruble' })
                )
            ),
            React.createElement(
                'div',
                { className: 'h4 col-xs-6 col-sm-1 col-md-1 col-lg-1 text-right' },
                sum,
                ' ',
                React.createElement('i', { className: 'fa fa-ruble' })
            ),
            React.createElement(
                'div',
                { className: 'col-xs-12 visible-xs hidden-sm hidden-md hidden-lg' },
                React.createElement('span', { dangerouslySetInnerHTML: { __html: this.props.product.name } }),
                React.createElement(
                    'sup',
                    { className: 'text-danger', style: { whiteSpace: 'nowrap' } },
                    ' ',
                    this.props.product.price,
                    ' ',
                    React.createElement('i', { className: 'fa fa-ruble' })
                )
            )
        );
    }
});

var BasketForm = React.createClass({
    displayName: 'BasketForm',

    mixins: [Reflux.listenTo(ClientStore, "onLoginChange")],
    onLoginChange: function onLoginChange(data) {
        this.setState(data);
    },
    getInitialState: function getInitialState() {
        return ClientStore.getInitialState();
    },
    handleChangeLogin: function handleChangeLogin(event) {
        actions.updateLogin(event.target.value, this.state.comment);
    },
    handleChangeComment: function handleChangeComment(event) {
        actions.updateLogin(this.state.login, event.target.value);
    },
    render: function render() {
        var login = this.state.login;
        var comment = this.state.comment;
        return React.createElement(
            'div',
            null,
            React.createElement('br', null),
            React.createElement(
                'div',
                { className: 'form-group' },
                React.createElement('input', { ref: 'telegram', value: login, onChange: this.handleChangeLogin,
                    type: 'text', id: 'contact', name: 'contact', className: 'form-control',
                    placeholder: '@telegram или номер телефона' })
            ),
            React.createElement(
                'div',
                { className: 'form-group' },
                React.createElement('textarea', { name: 'comment', value: comment, onChange: this.handleChangeComment,
                    id: 'comment', cols: '30', rows: '3', placeholder: 'Комментарий',
                    className: 'form-control' })
            )
        );
    },
    check: function check() {
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
    displayName: 'BasketList',

    mixins: [Reflux.listenTo(BasketStore, "onBasketChange")],
    onBasketChange: function onBasketChange(total) {
        this.setProps({ items: BasketStore.items(), total: BasketStore.totalSum() });
    },
    onClose: function onClose() {
        $(this.getDOMNode()).parents('#basket-list').slideToggle();
    },
    clearBusket: function clearBusket() {
        actions.clearBusket();
    },
    onSubmit: function onSubmit(event) {
        if (!this.refs.form.check()) event.preventDefault();
    },
    render: function render() {
        var self = this;
        var items = this.props.items;
        var list = items ? items.map(function (item) {
            item.key = item.product.id;return React.createElement(BasketLine, item);
        }) : '';
        var btn = this.props.link ? React.createElement(
            'button',
            { onClick: this.onSubmit, type: 'submit', target: 'orderForm', className: 'btn btn-success', href: this.props.link, alt: 'Потратить карму' },
            React.createElement('i', { className: 'fa fa-shopping-cart' }),
            '  Потратить'
        ) : '';
        var btn_cear = this.props.items && this.props.items.length > 0 ? React.createElement(
            'div',
            { onClick: this.clearBusket, className: 'btn btn-danger' },
            React.createElement('i', { className: 'fa fa-trash-o' }),
            '  Очистить'
        ) : '';
        var form = this.props.link ? React.createElement(BasketForm, { ref: 'form' }) : '';
        var karma = this.props.total > 0 ? React.createElement(
            'span',
            null,
            this.props.total,
            ' ',
            React.createElement('i', { className: 'fa fa-ruble' })
        ) : 'чиста';
        var csrf = this.props.csrf_token ? React.createElement('input', { type: 'hidden', name: 'csrfmiddlewaretoken', value: this.props.csrf_token }) : '';
        return items || this.props.link ? React.createElement(
            'div',
            { className: 'basket-list' },
            React.createElement(
                'form',
                { action: this.props.link, id: 'orderForm', method: 'POST' },
                csrf,
                React.createElement(
                    'div',
                    { className: 'panel panel-default' },
                    React.createElement(
                        'div',
                        { className: 'panel-body' },
                        React.createElement(
                            'div',
                            { className: 'container-fluid' },
                            list
                        ),
                        form
                    ),
                    React.createElement(
                        'div',
                        { className: 'panel-footer' },
                        React.createElement(
                            'div',
                            { className: 'row' },
                            React.createElement(
                                'span',
                                { className: 'h3 col-xs-12 col-sm-6 col-md-7 col-lg-8' },
                                'Ваша карма ',
                                karma
                            ),
                            React.createElement(
                                'div',
                                { className: 'h3 col-xs-12 col-sm-6 col-md-5 col-lg-4' },
                                React.createElement(
                                    'div',
                                    { className: 'btn-group' },
                                    btn,
                                    ' ',
                                    btn_cear,
                                    React.createElement(
                                        'div',
                                        { onClick: this.onClose, className: 'btn btn-default' },
                                        React.createElement('i', { className: 'fa fa-close' }),
                                        '  Закрыть'
                                    )
                                )
                            )
                        )
                    )
                )
            )
        ) : '';
    }
});

//# sourceMappingURL=shop.js.map