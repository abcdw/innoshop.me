#!/usr/bin/evn python
 # -*- coding: utf-8 -*-
 """Remove duplicate from pruducts"""
import json

def main():
    SKU = set()

    double =[]

    fi = open("../innoshop/fixtures/products.json")

    js = json.load(fi)
    fi.close()
    result=[]
    for x in js:
        SKF=x["fields"]["SKU"]
        if SKF in SKU:
            double.append(SKF)
        else:
            SKU.add(SKF)
            result.append(x)

    fi = open("../innoshop/fixtures/products.json","w")
    json.dump(result,fi)
    fi.close()

if __name__=='__main__':
    main()
