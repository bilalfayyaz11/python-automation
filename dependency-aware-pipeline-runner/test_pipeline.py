#!/usr/bin/env python3

import os


def test_successful_pipeline():
    print("\n" + "=" * 60)
    print("TEST 1: Successful Pipeline")
    print("=" * 60)
    os.system("python3 pipeline_runner.py pipeline_config.yaml")


def test_failed_pipeline():
    print("\n" + "=" * 60)
    print("TEST 2: Pipeline with Failure")
    print("=" * 60)
    os.system("python3 pipeline_runner.py pipeline_config_fail.yaml")


def test_complex_pipeline():
    print("\n" + "=" * 60)
    print("TEST 3: Complex Pipeline")
    print("=" * 60)
    os.system("python3 pipeline_runner.py pipeline_complex.yaml")


if __name__ == "__main__":
    test_successful_pipeline()
    test_failed_pipeline()
    test_complex_pipeline()
