#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Remove duplicate from pruducts"""
import json


def main():
    SKU = set()

    double = []

    js = ''
    with open("../innoshop/fixtures/products.json") as fi:
        js = json.load(fi)

    result = []
    for i, x in enumerate(js):
        SKF = x["fields"]["SKU"]
        if SKF in SKU:
            double.append(SKF)
        else:
            SKU.add(SKF)
            if x['fields']["description"] is None:
                x['fields']["description"] = ""
            result.append(x)
    print(double)
    fi = open("../innoshop/fixtures/products.json", "w")
    json.dump(result, fi)
    fi.close()

if __name__ == '__main__':
    main()
