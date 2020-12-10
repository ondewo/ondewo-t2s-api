# Release History
*****************
## Release ONDEWO T2S 1.3.0

### New Features
* [[OND232-81]](https://ondewo.atlassian.net/browse/OND232-81) -
Added GRPC config server. With this server it is possible to read and modify the configuration of the T2S service.
* [[OND232-37]](https://ondewo.atlassian.net/browse/OND232-37) -
Added apodization to generated audio as part of postprocessing
* [[OND232-114]](https://ondewo.atlassian.net/browse/OND232-37) -
Added different postprocessing techniques

### Improvements
* [[OND232-110]](https://ondewo.atlassian.net/browse/OND232-110) -
Added phonemization option for Glow-TTS
* [[OND232-88]](https://ondewo.atlassian.net/browse/OND232-88) -
Added support for Glow-TTS inference on Triton
* [[OND232-84]](https://ondewo.atlassian.net/browse/OND232-84) -
Added support for MB-MelGAN inference on Triton

### Bug fixes
* [[OND232-37]](https://ondewo.atlassian.net/browse/OND232-37) -
Fixed postprocessing to not add silence at the start of generated audio

### Migration Guide
* Change the config file to match the new structure.


*****************
## Release ONDEWO T2S 1.2.0

### New Features
* [[OND232-57]](https://ondewo.atlassian.net/browse/OND232-57) -
Added support for Glow-TTS model. Glow-TTS is a state-of-the-art model which produces high-quality mel-spectrograms from text.
* [[OND232-69]](https://ondewo.atlassian.net/browse/OND232-69) -
Added support for MB-MelGAN model. MB-MelGAN is a state-of-the-art model which produces high-quality audio from mel-spectrograms.

### Improvements
* [[OND232-75]](https://ondewo.atlassian.net/browse/OND232-75) -
Refactored inference module to support different combinations text-2-mel and mel-2-audio models.
* [[OND232-86]](https://ondewo.atlassian.net/browse/OND232-86) -
Migrated Triton server and client to 2.3.0.

### Bug fixes
* [[OND232-89]](https://ondewo.atlassian.net/browse/OND232-89) -
Fixed cythonization bug in creating release version of inference server.
* [[OND232-87]](https://ondewo.atlassian.net/browse/OND232-87) -
Fixed bug where English numbers were normalized as German

### Breaking Changes
* [[OND231-166]](https://ondewo.atlassian.net/browse/OND231-166) -
Due to inference refactoring the inference section of the config file has changed.

### Migration Guide
* Change the config file to match the new structure.


*****************
## Release ONDEWO T2S 1.1.1

### Improvements
* [[OND232-46]](https://ondewo.atlassian.net/browse/OND232-46) -
Migrated Triton server and client to 2.2.0.
* [[OND232-54]](https://ondewo.atlassian.net/browse/OND232-54) -
Migrated inference servers to CUDA 11.0
* [[OND232-72]](https://ondewo.atlassian.net/browse/OND232-72) -
Added URL normalization to normalization process.

### Migration Guide
* No extra steps necessary for migrating to this version.


*****************
## Release ONDEWO T2S 1.1.0

### New Features
* [[OND232-17]](https://ondewo.atlassian.net/browse/OND232-17) -
Added support for inference using Triton inference server.
* [[OND232-16]](https://ondewo.atlassian.net/browse/OND232-16) -
Added file and memory caching feature.
* [[OND232-50]](https://ondewo.atlassian.net/browse/OND232-50) -
Added a denoiser option for WaveGlow inference.

### Improvements
* [[OND232-40]](https://ondewo.atlassian.net/browse/OND232-40) -
Set up automatic packaging of releases.
* [[OND232-31]](https://ondewo.atlassian.net/browse/OND232-31) -
Migrated inference and training scripts for QuartzNet to NeMo 0.11.
* [[OND232-14]](https://ondewo.atlassian.net/browse/OND232-14) -
Created end-to-end tests to repository for batch and streaming servers.

### Breaking Changes
* [[OND232-17]](https://ondewo.atlassian.net/browse/OND232-17) -
Due to addition of Triton inference the inference section of the config file has changed.

### Migration Guide
* Change the config file to match the new structure.


*****************
## Release ONDEWO T2S 1.0.0
* First formal release issued
