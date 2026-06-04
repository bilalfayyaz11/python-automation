#!/bin/bash

VERSION="0.1.1"

calculate() {
    echo "Calculator v${VERSION}"
    echo "Result: $(($1 + $2))"
}

calculate "$@"
