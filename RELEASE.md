# Release History
*****************
## Release ONDEWO T2S API 5.1.0

### Improvements
 * Added documentation of the endpoints and messages
 * Moved CustomerPhonemizer endpoints to TextToSpeech service

*****************
## Release ONDEWO T2S API 5.0.0

### Improvements
 * Synchronize all API Client Versions

*****************

## Release ONDEWO T2S API 4.3.0

### Improvements
 * [[OND211-2039]](https://ondewo.atlassian.net/browse/OND211-2039) - Added pre-commit hooks and adjusted files to them

*****************
## Release ONDEWO T2S API 4.2.0

### Features
 * [[OND211-2039]](https://ondewo.atlassian.net/browse/OND211-2039) - Automated Release Process

*****************
## Release ONDEWO T2S API 4.1.0

### Features
* Added normalizer to synthesize message.

*****************
## Release ONDEWO T2S API 4.0.5

### Features
* Added callsign mapping.

*****************
## Release ONDEWO T2S API 4.0.4

### Features
* Fix mapping type, added callsign long and short to configuration file api.

*****************
## Release ONDEWO T2S API 4.0.3

### Features
* Add NormalizeText endpoint, that allows for text normalization without speech synthesis.

*****************
## Release ONDEWO T2S API 4.0.2

### Features
* Add field T2SCustomLengthScales to T2SNormalizePipeline.

*****************
## Release ONDEWO T2S API 4.0.1

### Features
 * [[OND232-348]](https://ondewo.atlassian.net/browse/OND232-348) - Add field normalized_text to SynthesizeResponse.

*****************

## Release ONDEWO T2S API 4.0.0

### Breaking Changes
 * [[OND232-343]](https://ondewo.atlassian.net/browse/OND232-343) - Rename oneof attributes and merged custom-phonemizer proto into text-to-speech proto

*****************
## Release ONDEWO T2S API 3.0.0

### Breaking Changes
 * [[OND231-334]](https://ondewo.atlassian.net/browse/OND231-334) - Rename Description, GetServiceInfoResponse, Inference and Normalization messages to include S2T

*****************

## Release ONDEWO T2S API 2.0.0

### Breaking Changes
`RequestConfig` implemented in SynthesizeRequest.

*****************

## Release ONDEWO T2S API 0.2.2

### Improvements
Updated README.

*****************
## Release ONDEWO T2S API 0.2.1

### Bug fixes
Updated licenses.

*****************
## Release ONDEWO T2S API 0.2.0

### New Features

Move to GitHub!

### Improvements

No longer closed source.

### Bug fixes

### Breaking Changes

### Known issues not covered in this release

### Migration Guide

[Replace submodule](https://stackoverflow.com/a/1260982/7756727) in the client.

*****************

## Release ONDEWO T2S API 0.1.0

### New Features

Refactored individual project APIs into seperate repos.

### Improvements

Easier to develop independently.

### Bug fixes

### Breaking Changes

### Known issues not covered in this release

Harder to install apis under one heading-- this will be addressed at a later date.

### Migration Guide

[Replace submodule](https://stackoverflow.com/a/1260982/7756727) in the client.

*****************
