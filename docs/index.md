# Protocol Documentation
<a name="top"></a>

## Table of Contents

- [ondewo/t2s/text-to-speech.proto](#ondewo/t2s/text-to-speech.proto)
    - [Apodization](#ondewo.t2s.Apodization)
    - [BatchSynthesizeRequest](#ondewo.t2s.BatchSynthesizeRequest)
    - [BatchSynthesizeResponse](#ondewo.t2s.BatchSynthesizeResponse)
    - [Caching](#ondewo.t2s.Caching)
    - [CompositeInference](#ondewo.t2s.CompositeInference)
    - [CreateCustomPhonemizerRequest](#ondewo.t2s.CreateCustomPhonemizerRequest)
    - [CustomPhonemizerProto](#ondewo.t2s.CustomPhonemizerProto)
    - [GlowTTS](#ondewo.t2s.GlowTTS)
    - [GlowTTSTriton](#ondewo.t2s.GlowTTSTriton)
    - [HiFiGan](#ondewo.t2s.HiFiGan)
    - [HiFiGanTriton](#ondewo.t2s.HiFiGanTriton)
    - [ListCustomPhonemizerRequest](#ondewo.t2s.ListCustomPhonemizerRequest)
    - [ListCustomPhonemizerResponse](#ondewo.t2s.ListCustomPhonemizerResponse)
    - [ListT2sDomainsRequest](#ondewo.t2s.ListT2sDomainsRequest)
    - [ListT2sDomainsResponse](#ondewo.t2s.ListT2sDomainsResponse)
    - [ListT2sLanguagesRequest](#ondewo.t2s.ListT2sLanguagesRequest)
    - [ListT2sLanguagesResponse](#ondewo.t2s.ListT2sLanguagesResponse)
    - [ListT2sPipelinesRequest](#ondewo.t2s.ListT2sPipelinesRequest)
    - [ListT2sPipelinesResponse](#ondewo.t2s.ListT2sPipelinesResponse)
    - [Logmnse](#ondewo.t2s.Logmnse)
    - [Map](#ondewo.t2s.Map)
    - [MbMelganTriton](#ondewo.t2s.MbMelganTriton)
    - [Mel2Audio](#ondewo.t2s.Mel2Audio)
    - [NormalizeTextRequest](#ondewo.t2s.NormalizeTextRequest)
    - [NormalizeTextResponse](#ondewo.t2s.NormalizeTextResponse)
    - [PhonemizerId](#ondewo.t2s.PhonemizerId)
    - [Postprocessing](#ondewo.t2s.Postprocessing)
    - [RequestConfig](#ondewo.t2s.RequestConfig)
    - [SynthesizeRequest](#ondewo.t2s.SynthesizeRequest)
    - [SynthesizeResponse](#ondewo.t2s.SynthesizeResponse)
    - [T2SCustomLengthScales](#ondewo.t2s.T2SCustomLengthScales)
    - [T2SDescription](#ondewo.t2s.T2SDescription)
    - [T2SGetServiceInfoResponse](#ondewo.t2s.T2SGetServiceInfoResponse)
    - [T2SInference](#ondewo.t2s.T2SInference)
    - [T2SNormalization](#ondewo.t2s.T2SNormalization)
    - [T2sPipelineId](#ondewo.t2s.T2sPipelineId)
    - [Text2Mel](#ondewo.t2s.Text2Mel)
    - [Text2SpeechConfig](#ondewo.t2s.Text2SpeechConfig)
    - [UpdateCustomPhonemizerRequest](#ondewo.t2s.UpdateCustomPhonemizerRequest)
    - [Wiener](#ondewo.t2s.Wiener)
  
    - [AudioFormat](#ondewo.t2s.AudioFormat)
    - [Pcm](#ondewo.t2s.Pcm)
    - [UpdateCustomPhonemizerRequest.UpdateMethod](#ondewo.t2s.UpdateCustomPhonemizerRequest.UpdateMethod)
  
    - [CustomPhonemizers](#ondewo.t2s.CustomPhonemizers)
    - [Text2Speech](#ondewo.t2s.Text2Speech)
  
- [Scalar Value Types](#scalar-value-types)



<a name="ondewo/t2s/text-to-speech.proto"></a>
<p align="right"><a href="#top">Top</a></p>

## ondewo/t2s/text-to-speech.proto



<a name="ondewo.t2s.Apodization"></a>

### Apodization



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| apodization_secs | [float](#float) |  |  |






<a name="ondewo.t2s.BatchSynthesizeRequest"></a>

### BatchSynthesizeRequest



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| batch_request | [SynthesizeRequest](#ondewo.t2s.SynthesizeRequest) | repeated |  |






<a name="ondewo.t2s.BatchSynthesizeResponse"></a>

### BatchSynthesizeResponse



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| batch_response | [SynthesizeResponse](#ondewo.t2s.SynthesizeResponse) | repeated |  |






<a name="ondewo.t2s.Caching"></a>

### Caching



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| active | [bool](#bool) |  |  |
| memory_cache_max_size | [int64](#int64) |  |  |
| sampling_rate | [int64](#int64) |  |  |
| load_cache | [bool](#bool) |  |  |
| save_cache | [bool](#bool) |  |  |
| cache_save_dir | [string](#string) |  |  |






<a name="ondewo.t2s.CompositeInference"></a>

### CompositeInference



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| text2mel | [Text2Mel](#ondewo.t2s.Text2Mel) |  |  |
| mel2audio | [Mel2Audio](#ondewo.t2s.Mel2Audio) |  |  |






<a name="ondewo.t2s.CreateCustomPhonemizerRequest"></a>

### CreateCustomPhonemizerRequest



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| prefix | [string](#string) |  |  |
| maps | [Map](#ondewo.t2s.Map) | repeated |  |






<a name="ondewo.t2s.CustomPhonemizerProto"></a>

### CustomPhonemizerProto



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| id | [string](#string) |  |  |
| maps | [Map](#ondewo.t2s.Map) | repeated |  |






<a name="ondewo.t2s.GlowTTS"></a>

### GlowTTS



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| batch_size | [int64](#int64) |  |  |
| use_gpu | [bool](#bool) |  |  |
| length_scale | [float](#float) |  |  |
| noise_scale | [float](#float) |  |  |
| path | [string](#string) |  |  |
| cleaners | [string](#string) | repeated |  |
| param_config_path | [string](#string) |  |  |






<a name="ondewo.t2s.GlowTTSTriton"></a>

### GlowTTSTriton



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| batch_size | [int64](#int64) |  |  |
| length_scale | [float](#float) |  |  |
| noise_scale | [float](#float) |  |  |
| cleaners | [string](#string) | repeated |  |
| max_text_length | [int64](#int64) |  |  |
| param_config_path | [string](#string) |  |  |
| triton_model_name | [string](#string) |  |  |






<a name="ondewo.t2s.HiFiGan"></a>

### HiFiGan



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| use_gpu | [bool](#bool) |  |  |
| batch_size | [int64](#int64) |  |  |
| config_path | [string](#string) |  |  |
| model_path | [string](#string) |  |  |






<a name="ondewo.t2s.HiFiGanTriton"></a>

### HiFiGanTriton



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| config_path | [string](#string) |  |  |
| triton_model_name | [string](#string) |  |  |






<a name="ondewo.t2s.ListCustomPhonemizerRequest"></a>

### ListCustomPhonemizerRequest



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| pipeline_ids | [string](#string) | repeated |  |






<a name="ondewo.t2s.ListCustomPhonemizerResponse"></a>

### ListCustomPhonemizerResponse



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| phonemizers | [CustomPhonemizerProto](#ondewo.t2s.CustomPhonemizerProto) | repeated |  |






<a name="ondewo.t2s.ListT2sDomainsRequest"></a>

### ListT2sDomainsRequest
Domain Request representation.
The request message for ListT2sDomains.
Filter domains of pipelines by attributed in request.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| speaker_sexes | [string](#string) | repeated | Optional. Define the speaker sex. |
| pipeline_owners | [string](#string) | repeated | Optional. Define the pipeline owner/ owners. |
| speaker_names | [string](#string) | repeated | Optional. Define the speaker name/ names. |
| languages | [string](#string) | repeated | Optional. Define the language/ languages. |






<a name="ondewo.t2s.ListT2sDomainsResponse"></a>

### ListT2sDomainsResponse
Domains Response representation.
The response message for ListT2sDomains.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| domains | [string](#string) | repeated | Required. Define the domain/ domains that satisfy/ies the specifications in the ListT2sDomainsRequest. |






<a name="ondewo.t2s.ListT2sLanguagesRequest"></a>

### ListT2sLanguagesRequest
Language Request representation.
The request message for ListT2sLanguages.
Filter languages of pipelines by attributed in request.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| speaker_sexes | [string](#string) | repeated | Optional. Define the speaker sex. |
| pipeline_owners | [string](#string) | repeated | Optional. Define the pipeline owner/ owners. |
| speaker_names | [string](#string) | repeated | Optional. Define the speaker name/ names. |
| domains | [string](#string) | repeated | Optional. Define the domain/ domains. |






<a name="ondewo.t2s.ListT2sLanguagesResponse"></a>

### ListT2sLanguagesResponse
Language Response representation.
The response message for ListT2sLanguages.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| languages | [string](#string) | repeated | Required. Define the language/ languages that satisfy/ies the specifications in the ListT2sLanguagesRequest. |






<a name="ondewo.t2s.ListT2sPipelinesRequest"></a>

### ListT2sPipelinesRequest
Pipeline Request representation.
The request message for ListT2sPipelines.
Filter pipelines by attributed in request.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| languages | [string](#string) | repeated | Optional. Define the language/ languages. |
| speaker_sexes | [string](#string) | repeated | Optional. Define the speaker sex. |
| pipeline_owners | [string](#string) | repeated | Optional. Define the pipeline owner/ owners. |
| speaker_names | [string](#string) | repeated | Optional. Define the speaker name/ names. |
| domains | [string](#string) | repeated | Optional. Define the domain/ domains. |






<a name="ondewo.t2s.ListT2sPipelinesResponse"></a>

### ListT2sPipelinesResponse
Pipeline Response representation.
The response message for ListT2sPipelines.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| pipelines | [Text2SpeechConfig](#ondewo.t2s.Text2SpeechConfig) | repeated | Required. Representation of a list of pipelines configurations. Retrieved by ListT2sPipelines, containing the configurations of pipelines with the specifications received in the ListT2sPipelinesRequest. |






<a name="ondewo.t2s.Logmnse"></a>

### Logmnse



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| initial_noise | [int64](#int64) |  |  |
| window_size | [int64](#int64) |  |  |
| noise_threshold | [float](#float) |  |  |






<a name="ondewo.t2s.Map"></a>

### Map



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| word | [string](#string) |  |  |
| phoneme_groups | [string](#string) |  |  |






<a name="ondewo.t2s.MbMelganTriton"></a>

### MbMelganTriton



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| config_path | [string](#string) |  |  |
| stats_path | [string](#string) |  |  |
| triton_model_name | [string](#string) |  |  |
| triton_url | [string](#string) |  |  |






<a name="ondewo.t2s.Mel2Audio"></a>

### Mel2Audio



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| type | [string](#string) |  |  |
| mb_melgan_triton | [MbMelganTriton](#ondewo.t2s.MbMelganTriton) |  |  |
| hifi_gan | [HiFiGan](#ondewo.t2s.HiFiGan) |  |  |
| hifi_gan_triton | [HiFiGanTriton](#ondewo.t2s.HiFiGanTriton) |  |  |






<a name="ondewo.t2s.NormalizeTextRequest"></a>

### NormalizeTextRequest



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| t2s_pipeline_id | [string](#string) |  |  |
| text | [string](#string) |  |  |






<a name="ondewo.t2s.NormalizeTextResponse"></a>

### NormalizeTextResponse



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| normalized_text | [string](#string) |  |  |






<a name="ondewo.t2s.PhonemizerId"></a>

### PhonemizerId



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| id | [string](#string) |  |  |






<a name="ondewo.t2s.Postprocessing"></a>

### Postprocessing



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| silence_secs | [float](#float) |  |  |
| pipeline | [string](#string) | repeated |  |
| logmmse | [Logmnse](#ondewo.t2s.Logmnse) |  |  |
| wiener | [Wiener](#ondewo.t2s.Wiener) |  |  |
| apodization | [Apodization](#ondewo.t2s.Apodization) |  |  |






<a name="ondewo.t2s.RequestConfig"></a>

### RequestConfig
Represents a Configuration for the text to speech conversion.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| t2s_pipeline_id | [string](#string) |  | Required. Represents the pipeline id of the model configuration that will be used. |
| length_scale | [float](#float) |  |  |
| noise_scale | [float](#float) |  |  |
| sample_rate | [int32](#int32) |  |  |
| pcm | [Pcm](#ondewo.t2s.Pcm) |  |  |
| audio_format | [AudioFormat](#ondewo.t2s.AudioFormat) |  |  |
| use_cache | [bool](#bool) |  |  |
| normalizer | [string](#string) |  |  |






<a name="ondewo.t2s.SynthesizeRequest"></a>

### SynthesizeRequest
Represents a Synthesize Request.
A Synthesize Request contains the information need to perform a text to speech conversion.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| text | [string](#string) |  | Required. Represents the text that will be transformed to speech. |
| config | [RequestConfig](#ondewo.t2s.RequestConfig) |  | Required. Represents the specifications needed to do the text to speech transformation. |






<a name="ondewo.t2s.SynthesizeResponse"></a>

### SynthesizeResponse
Represents a Synthesize Response.
A Synthesize Request contains the converted text to audio and the requested configuration.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| audio_uuid | [string](#string) |  | Required. Represents the pipeline id of the model configuration that will be used. |
| audio | [bytes](#bytes) |  | Required. Generated file with the parameters described in request. |
| generation_time | [float](#float) |  | Required. Time to generate audio. |
| audio_length | [float](#float) |  | Required. Audio length. |
| text | [string](#string) |  | Required. Text from which audio was generated. |
| config | [RequestConfig](#ondewo.t2s.RequestConfig) |  | Required. Configuration from which audio was generated. |
| normalized_text | [string](#string) |  | Optional. Normalized text. |






<a name="ondewo.t2s.T2SCustomLengthScales"></a>

### T2SCustomLengthScales



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| text | [float](#float) |  |  |
| email | [float](#float) |  |  |
| url | [float](#float) |  |  |
| phone | [float](#float) |  |  |
| spell | [float](#float) |  |  |
| spell_with_names | [float](#float) |  |  |
| callsign_long | [float](#float) |  |  |
| callsign_short | [float](#float) |  |  |






<a name="ondewo.t2s.T2SDescription"></a>

### T2SDescription



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| language | [string](#string) |  |  |
| speaker_sex | [string](#string) |  |  |
| pipeline_owner | [string](#string) |  |  |
| comments | [string](#string) |  |  |
| speaker_name | [string](#string) |  |  |
| domain | [string](#string) |  |  |






<a name="ondewo.t2s.T2SGetServiceInfoResponse"></a>

### T2SGetServiceInfoResponse



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| version | [string](#string) |  |  |






<a name="ondewo.t2s.T2SInference"></a>

### T2SInference



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| type | [string](#string) |  |  |
| composite_inference | [CompositeInference](#ondewo.t2s.CompositeInference) |  |  |
| caching | [Caching](#ondewo.t2s.Caching) |  |  |






<a name="ondewo.t2s.T2SNormalization"></a>

### T2SNormalization



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| language | [string](#string) |  |  |
| pipeline | [string](#string) | repeated |  |
| custom_phonemizer_id | [string](#string) |  |  |
| custom_length_scales | [T2SCustomLengthScales](#ondewo.t2s.T2SCustomLengthScales) |  |  |
| arpabet_mapping | [string](#string) |  |  |
| numeric_mapping | [string](#string) |  |  |
| callsigns_mapping | [string](#string) |  |  |






<a name="ondewo.t2s.T2sPipelineId"></a>

### T2sPipelineId
Pipeline Id representation.
Used in the creation, deletion and getter of pipelines.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| id | [string](#string) |  | Required. Defines the id of the pipeline. |






<a name="ondewo.t2s.Text2Mel"></a>

### Text2Mel



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| type | [string](#string) |  |  |
| glow_tts | [GlowTTS](#ondewo.t2s.GlowTTS) |  |  |
| glow_tts_triton | [GlowTTSTriton](#ondewo.t2s.GlowTTSTriton) |  |  |






<a name="ondewo.t2s.Text2SpeechConfig"></a>

### Text2SpeechConfig
Configuration of text-to-speech models representation.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| id | [string](#string) |  | Required. Defines the id of the pipeline. |
| description | [T2SDescription](#ondewo.t2s.T2SDescription) |  | Required. Defines the description of the pipeline representation. |
| active | [bool](#bool) |  | Required. Defines if the pipeline is active or inactive. |
| inference | [T2SInference](#ondewo.t2s.T2SInference) |  | Required. Defines he inference of the pipeline representation. |
| normalization | [T2SNormalization](#ondewo.t2s.T2SNormalization) |  | Required. Defines the normalization process of the pipeline representation. |
| postprocessing | [Postprocessing](#ondewo.t2s.Postprocessing) |  | Required. Defines the postprocessing process of the pipeline representation. |






<a name="ondewo.t2s.UpdateCustomPhonemizerRequest"></a>

### UpdateCustomPhonemizerRequest



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| id | [string](#string) |  |  |
| update_method | [UpdateCustomPhonemizerRequest.UpdateMethod](#ondewo.t2s.UpdateCustomPhonemizerRequest.UpdateMethod) |  |  |
| maps | [Map](#ondewo.t2s.Map) | repeated |  |






<a name="ondewo.t2s.Wiener"></a>

### Wiener



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| frame_len | [int64](#int64) |  |  |
| lpc_order | [int64](#int64) |  |  |
| iterations | [int64](#int64) |  |  |
| alpha | [float](#float) |  |  |
| thresh | [float](#float) |  |  |





 <!-- end messages -->


<a name="ondewo.t2s.AudioFormat"></a>

### AudioFormat
Represents an audio file format, which is a file format for storing
digital audio data on a computer system.

| Name | Number | Description |
| ---- | ------ | ----------- |
| wav | 0 |  |
| flac | 1 |  |
| caf | 2 |  |
| mp3 | 3 |  |
| aac | 4 |  |
| ogg | 5 |  |
| wma | 6 |  |



<a name="ondewo.t2s.Pcm"></a>

### Pcm
Represents a pulse-code modulation technique.

| Name | Number | Description |
| ---- | ------ | ----------- |
| PCM_16 | 0 |  |
| PCM_24 | 1 |  |
| PCM_32 | 2 |  |
| PCM_S8 | 3 |  |
| PCM_U8 | 4 |  |
| FLOAT | 5 |  |
| DOUBLE | 6 |  |



<a name="ondewo.t2s.UpdateCustomPhonemizerRequest.UpdateMethod"></a>

### UpdateCustomPhonemizerRequest.UpdateMethod
extend hard will add new words replacing those that are already in phonemizer
extend soft will add new words only if they are not yet in phonemizer
replace will clean all the words in the phonemizer and then add new ones

| Name | Number | Description |
| ---- | ------ | ----------- |
| extend_hard | 0 |  |
| extend_soft | 1 |  |
| replace | 2 |  |


 <!-- end enums -->

 <!-- end HasExtensions -->


<a name="ondewo.t2s.CustomPhonemizers"></a>

### CustomPhonemizers
endpoints of custom phonemizer

| Method Name | Request Type | Response Type | Description |
| ----------- | ------------ | ------------- | ------------|
| GetCustomPhonemizer | [PhonemizerId](#ondewo.t2s.PhonemizerId) | [CustomPhonemizerProto](#ondewo.t2s.CustomPhonemizerProto) |  |
| CreateCustomPhonemizer | [CreateCustomPhonemizerRequest](#ondewo.t2s.CreateCustomPhonemizerRequest) | [PhonemizerId](#ondewo.t2s.PhonemizerId) |  |
| DeleteCustomPhonemizer | [PhonemizerId](#ondewo.t2s.PhonemizerId) | [.google.protobuf.Empty](#google.protobuf.Empty) |  |
| UpdateCustomPhonemizer | [UpdateCustomPhonemizerRequest](#ondewo.t2s.UpdateCustomPhonemizerRequest) | [CustomPhonemizerProto](#ondewo.t2s.CustomPhonemizerProto) |  |
| ListCustomPhonemizer | [ListCustomPhonemizerRequest](#ondewo.t2s.ListCustomPhonemizerRequest) | [ListCustomPhonemizerResponse](#ondewo.t2s.ListCustomPhonemizerResponse) |  |


<a name="ondewo.t2s.Text2Speech"></a>

### Text2Speech
endpoints of t2s generate service

| Method Name | Request Type | Response Type | Description |
| ----------- | ------------ | ------------- | ------------|
| Synthesize | [SynthesizeRequest](#ondewo.t2s.SynthesizeRequest) | [SynthesizeResponse](#ondewo.t2s.SynthesizeResponse) | Synthesizes an specific text sent in the request with the configuration requirements and retrieves a response that includes the synthesized text to audio and the configuration wanted. |
| BatchSynthesize | [BatchSynthesizeRequest](#ondewo.t2s.BatchSynthesizeRequest) | [BatchSynthesizeResponse](#ondewo.t2s.BatchSynthesizeResponse) | will this safe time when doing batch predict on the AI model? |
| NormalizeText | [NormalizeTextRequest](#ondewo.t2s.NormalizeTextRequest) | [NormalizeTextResponse](#ondewo.t2s.NormalizeTextResponse) | Normalize a text according to a specific pipeline normalization rules. |
| GetT2sPipeline | [T2sPipelineId](#ondewo.t2s.T2sPipelineId) | [Text2SpeechConfig](#ondewo.t2s.Text2SpeechConfig) | Retrieves the configuration of the specified pipeline. |
| CreateT2sPipeline | [Text2SpeechConfig](#ondewo.t2s.Text2SpeechConfig) | [T2sPipelineId](#ondewo.t2s.T2sPipelineId) | Creates a pipeline with the specified configuration and retrieves its id. |
| DeleteT2sPipeline | [T2sPipelineId](#ondewo.t2s.T2sPipelineId) | [.google.protobuf.Empty](#google.protobuf.Empty) | Deletes the specified pipeline. |
| UpdateT2sPipeline | [Text2SpeechConfig](#ondewo.t2s.Text2SpeechConfig) | [.google.protobuf.Empty](#google.protobuf.Empty) | Update a specified pipeline with certain configuration. |
| ListT2sPipelines | [ListT2sPipelinesRequest](#ondewo.t2s.ListT2sPipelinesRequest) | [ListT2sPipelinesResponse](#ondewo.t2s.ListT2sPipelinesResponse) | Retrieve the list of pipelines with an specific requirement. |
| ListT2sLanguages | [ListT2sLanguagesRequest](#ondewo.t2s.ListT2sLanguagesRequest) | [ListT2sLanguagesResponse](#ondewo.t2s.ListT2sLanguagesResponse) | Retrieve the list of languages given a specific config request. |
| ListT2sDomains | [ListT2sDomainsRequest](#ondewo.t2s.ListT2sDomainsRequest) | [ListT2sDomainsResponse](#ondewo.t2s.ListT2sDomainsResponse) | Retrieve the list of domains given a specific config request. |
| GetServiceInfo | [.google.protobuf.Empty](#google.protobuf.Empty) | [T2SGetServiceInfoResponse](#ondewo.t2s.T2SGetServiceInfoResponse) | Returns a message containing the version of the running text to speech server. |

 <!-- end services -->



## Scalar Value Types

| .proto Type | Notes | C++ | Java | Python | Go | C# | PHP | Ruby |
| ----------- | ----- | --- | ---- | ------ | -- | -- | --- | ---- |
| <a name="double" /> double |  | double | double | float | float64 | double | float | Float |
| <a name="float" /> float |  | float | float | float | float32 | float | float | Float |
| <a name="int32" /> int32 | Uses variable-length encoding. Inefficient for encoding negative numbers – if your field is likely to have negative values, use sint32 instead. | int32 | int | int | int32 | int | integer | Bignum or Fixnum (as required) |
| <a name="int64" /> int64 | Uses variable-length encoding. Inefficient for encoding negative numbers – if your field is likely to have negative values, use sint64 instead. | int64 | long | int/long | int64 | long | integer/string | Bignum |
| <a name="uint32" /> uint32 | Uses variable-length encoding. | uint32 | int | int/long | uint32 | uint | integer | Bignum or Fixnum (as required) |
| <a name="uint64" /> uint64 | Uses variable-length encoding. | uint64 | long | int/long | uint64 | ulong | integer/string | Bignum or Fixnum (as required) |
| <a name="sint32" /> sint32 | Uses variable-length encoding. Signed int value. These more efficiently encode negative numbers than regular int32s. | int32 | int | int | int32 | int | integer | Bignum or Fixnum (as required) |
| <a name="sint64" /> sint64 | Uses variable-length encoding. Signed int value. These more efficiently encode negative numbers than regular int64s. | int64 | long | int/long | int64 | long | integer/string | Bignum |
| <a name="fixed32" /> fixed32 | Always four bytes. More efficient than uint32 if values are often greater than 2^28. | uint32 | int | int | uint32 | uint | integer | Bignum or Fixnum (as required) |
| <a name="fixed64" /> fixed64 | Always eight bytes. More efficient than uint64 if values are often greater than 2^56. | uint64 | long | int/long | uint64 | ulong | integer/string | Bignum |
| <a name="sfixed32" /> sfixed32 | Always four bytes. | int32 | int | int | int32 | int | integer | Bignum or Fixnum (as required) |
| <a name="sfixed64" /> sfixed64 | Always eight bytes. | int64 | long | int/long | int64 | long | integer/string | Bignum |
| <a name="bool" /> bool |  | bool | boolean | boolean | bool | bool | boolean | TrueClass/FalseClass |
| <a name="string" /> string | A string must always contain UTF-8 encoded or 7-bit ASCII text. | string | String | str/unicode | string | string | string | String (UTF-8) |
| <a name="bytes" /> bytes | May contain any arbitrary sequence of bytes. | string | ByteString | str | []byte | ByteString | string | String (ASCII-8BIT) |
