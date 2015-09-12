'use strict';

var actions = Reflux.createActions(['addToBasket', 'decFromBasket']);

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

var BasketStore = Reflux.createStore({
    init: function init() {
        this.data = [];
        this.listenTo(actions.addToBasket, this.onAddToBasket);
        this.listenTo(actions.decFromBasket, this.onDecFromBasket);
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
    onDecFromBasket: function onDecFromBasket(id, remove) {
        if (this.data[id]) {
            var cnt = remove ? this.data[id].count : 1;
            this.data[id].count = this.data[id].count - cnt;
            if (this.data[id].count <= 0) delete this.data[id];
            $.get(this.url + '?id=' + id + '&count=-' + cnt, function (res) {});
            this.trigger(this.totalSum());
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
                React.createElement('i', { className: 'fa fa-shopping-cart' }),
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
                this.props.count
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

var BasketList = React.createClass({
    displayName: 'BasketList',

    mixins: [Reflux.listenTo(BasketStore, "onBasketChange")],
    onBasketChange: function onBasketChange(total) {
        this.setProps({ items: BasketStore.items(), total: BasketStore.totalSum() });
    },
    render: function render() {
        var self = this;
        var items = this.props.items;
        var list = items ? items.map(function (item) {
            item.key = item.product.id;return React.createElement(BasketLine, item);
        }) : '';
        var btn = this.props.link ? React.createElement(
            'button',
            { type: 'submit', target: 'orderForm', className: 'btn btn-info', href: this.props.link, alt: 'Потратить карму' },
            React.createElement('i', { className: 'fa fa-shopping-cart' }),
            '  Потратить'
        ) : '';

        var form = this.props.link ? React.createElement(
            'div',
            null,
            React.createElement('br', null),
            React.createElement(
                'div',
                { className: 'form-group' },
                React.createElement('input', { type: 'text', id: 'contact', name: 'contact', className: 'form-control',
                    placeholder: '@telegram или номер телефона' })
            ),
            React.createElement(
                'div',
                { className: 'form-group' },
                React.createElement('textarea', { name: 'comment', id: 'comment', cols: '30', rows: '3', placeholder: 'Комментарий',
                    className: 'form-control' })
            )
        ) : '';
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
                                { className: 'h3 col-xs-12 col-sm-10 col-md-10 col-lg-10' },
                                'Ваша карма ',
                                this.props.total,
                                ' ',
                                React.createElement('i', { className: 'fa fa-ruble' })
                            ),
                            React.createElement(
                                'div',
                                { className: 'h3 col-xs-12 col-sm-2 col-md-2 col-lg-2' },
                                btn
                            )
                        )
                    )
                )
            )
        ) : '';
    }
});

//# sourceMappingURL=shop.js.map