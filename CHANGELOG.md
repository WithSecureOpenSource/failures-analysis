# Changelog

<!--next-version-placeholder-->

## v2.0.2 (2022-06-17)
### Fix
* Return support for Python 3.8 ([`6bc2b1b`](https://github.com/F-Secure/failures-analysis/commit/6bc2b1b0f356bfc7fbd3b3c7297f64c4ccbce105))

## v2.0.1 (2022-06-17)
### Fix
* If Drain3 is used, display original error ([`e75dfaa`](https://github.com/F-Secure/failures-analysis/commit/e75dfaac0ee98675b6aabf0708f111625dfc7e3f))

## v2.0.0 (2022-06-17)
### Feature
* Use Drain3 to template failure messages ([`efe9538`](https://github.com/F-Secure/failures-analysis/commit/efe9538f8131d918ab88230737d811907af045cc))

### Breaking
* FIll use by default Drain3 to template error messages  ([`efe9538`](https://github.com/F-Secure/failures-analysis/commit/efe9538f8131d918ab88230737d811907af045cc))

## v1.1.0 (2022-06-17)
### Feature
* Add possibility to define minimum similarity ([`7bfa099`](https://github.com/F-Secure/failures-analysis/commit/7bfa09933188f35c7fe084a328acfabbc05ff009))

## v1.0.5 (2022-06-16)
### Fix
* Small performance improvement ([`8d85431`](https://github.com/F-Secure/failures-analysis/commit/8d854313105cc1e10bc54429d4f6c1acaf4749be))

## v1.0.4 (2022-06-16)
### Fix
* Fix for printing all rows ([`2fd01e3`](https://github.com/F-Secure/failures-analysis/commit/2fd01e3b4c822947b4c2227fdac81d060ce0ca8a))
* Further improvent to the timeout issue ([`d4236c5`](https://github.com/F-Secure/failures-analysis/commit/d4236c5e2ac929511d4eaafeb29a15f6f570b2fd))

## v1.0.3 (2022-06-07)
### Fix
* Remove not used dependecies from pyproject.toml ([`e352da4`](https://github.com/F-Secure/failures-analysis/commit/e352da4b981d3391ce02da901c8665875b95ca06))
* Fix for the linting issue ([`581882a`](https://github.com/F-Secure/failures-analysis/commit/581882a1494235acca661c3910eee70fec4bd292))
* Fix for a test_score_similiarity to take in account latest changes in the failure_analysis.py ([`4714009`](https://github.com/F-Secure/failures-analysis/commit/4714009f17e73390ef6e2d693432ffb715f91e1f))
* Possible fix for a time-out issue, by commenting out other string similiarity algorithms but cosine similiarity. ([`e253d96`](https://github.com/F-Secure/failures-analysis/commit/e253d96e9e82ec9767a4f42dc397bf0edab0469e))

### Documentation
* Update usage instructions ([`de4e4b1`](https://github.com/F-Secure/failures-analysis/commit/de4e4b1e4b8fd197570d9e7888bea0952fff50e3))

## v1.0.2 (2022-06-07)
### Fix
* Fix for a fix to support 2 frameworks ([`5063ca3`](https://github.com/F-Secure/failures-analysis/commit/5063ca3cfd8f38b8dd420fb736ddcd68a5dbe00a))
* Fix to support both robotframework and pytest  ([`d9d57ad`](https://github.com/F-Secure/failures-analysis/commit/d9d57adafaf3663efd322ffdb73e95a774f4467e))

## v1.0.1 (2022-06-07)
### Fix
* Reading error message ([`60ba117`](https://github.com/F-Secure/failures-analysis/commit/60ba117feecde4f8a0dc0f79de17d29843d45609))
* Do not parse folder with lxml ([`1bfb32c`](https://github.com/F-Secure/failures-analysis/commit/1bfb32c4ba62cc011909bf5c24d6f0689882ea01))
* Fix to AttributeError: 'SequenceMatcher' object has no attribute 'matching_blocks'  ([`195e671`](https://github.com/F-Secure/failures-analysis/commit/195e671f0f418ac17b54d3927f98468da8007312))

### Documentation
* Update install instructions ([`cc084b4`](https://github.com/F-Secure/failures-analysis/commit/cc084b4531f02598304e5c3ddeea484ef950efc1))

## v1.0.0 (2022-06-05)
### Feature
* Change etry point name ([`ede8538`](https://github.com/F-Secure/failures-analysis/commit/ede853860eb9628e0f388ea56a7c39d40ff76cf5))

### Breaking
* update entry point runner  ([`ede8538`](https://github.com/F-Secure/failures-analysis/commit/ede853860eb9628e0f388ea56a7c39d40ff76cf5))

### Documentation
* CHANGELOG.md remove not user visible change ([`421dae3`](https://github.com/F-Secure/failures-analysis/commit/421dae301fa28507f006ffc5d6cb5508ebb81bb8))

## v0.2.3 (2022-06-01)
### Fix
* Fix for no failures found case ([`b45715e`](https://github.com/F-Secure/failures-analysis/commit/b45715ea0cbee5b90f3244cbf851482500939b3c))

## v0.2.2 (2022-05-31)
### Fix
* Better failure if xunit path is not found ([`2f2bd6a`](https://github.com/F-Secure/failures-analysis/commit/2f2bd6a761864723d4e4a688e10296f06a4ea83a))
* Reading xml files from folder ([`dcef437`](https://github.com/F-Secure/failures-analysis/commit/dcef43755dac43a11db3c4d8304f5fed2640a7d6))

## v0.2.1 (2022-05-30)
### Fix
* Build by poetry ([`0c86dce`](https://github.com/F-Secure/failures-analysis/commit/0c86dced450c4865469a657502e024637f7e079b))

## v0.2.0 (2022-05-30)
### Feature
* Automatic release ([`e55530e`](https://github.com/F-Secure/failures-analysis/commit/e55530e4877d4de2bc395d61fa6a788ecfa1cd2f))
* Classifiers and entry point ([`2991286`](https://github.com/F-Secure/failures-analysis/commit/2991286a41865b3306907dacce9f4622ceb882a6))
* Entry point for console script ([`966e292`](https://github.com/F-Secure/failures-analysis/commit/966e292c4521001cc37528a73977be902c16248d))

### Fix
* Freeze  python-semantic-release ([`d02b7be`](https://github.com/F-Secure/failures-analysis/commit/d02b7be30191d6cfbaea8c78b5a6bcb557fa14cd))
* Add logging for release ([`bacbec0`](https://github.com/F-Secure/failures-analysis/commit/bacbec09d8a2b8e7d32959c8ff453976f22449a5))
* Description too long in pyproject.toml for publish ([`df501a8`](https://github.com/F-Secure/failures-analysis/commit/df501a8a4b05914819d96003ab3e9638f00c0263))
* Description too long in pyproject.toml for publish ([`d54a62a`](https://github.com/F-Secure/failures-analysis/commit/d54a62ad356aed9293f3f56bf9a791878d028c9b))
* Remove jellyfish warning ([`13f86c9`](https://github.com/F-Secure/failures-analysis/commit/13f86c937645e268aac3096da06b0ec5e1769362))
* Invalid entry point definition ([`91fe7d4`](https://github.com/F-Secure/failures-analysis/commit/91fe7d4a914ad5b2aa9899437632928534fc3974))
* Fail if path is not file ([`e823d44`](https://github.com/F-Secure/failures-analysis/commit/e823d448180bdf46b056463031a605b0eff8f479))
* Use argument parser to parsing args ([`f388922`](https://github.com/F-Secure/failures-analysis/commit/f38892257c9f43e44429f15569e6aebb1a3d1adb))

### Documentation
* Improcing pyproject file ([`fac563f`](https://github.com/F-Secure/failures-analysis/commit/fac563f88d5ca0873b3e96082953106b81cc2742))
* Add CONTRIBUTING.md ([`0c27e2a`](https://github.com/F-Secure/failures-analysis/commit/0c27e2a01060a1ca67b6425982c42a994d532c84))
