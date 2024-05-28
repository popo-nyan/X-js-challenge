let _element = {
    appendChild: function (tag) {
    },
    removeChild: function (tag) {
    },
    setAttribute: function (tag, value) {
    },

};
_element.children = [_element];
_element.lastElementChild = _element;
_element.parentNode = _element;
document = {
    createElement: function (tag) {
        return _element;
    },
    getElementsByTagName: function (tag) {
        return [_element];
    }
};