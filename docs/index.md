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
    - [ListT2sNormalizationPipelinesRequest](#ondewo.t2s.ListT2sNormalizationPipelinesRequest)
    - [ListT2sNormalizationPipelinesResponse](#ondewo.t2s.ListT2sNormalizationPipelinesResponse)
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
    - [SingleInference](#ondewo.t2s.SingleInference)
    - [StreamingSynthesizeRequest](#ondewo.t2s.StreamingSynthesizeRequest)
    - [StreamingSynthesizeResponse](#ondewo.t2s.StreamingSynthesizeResponse)
    - [SynthesizeRequest](#ondewo.t2s.SynthesizeRequest)
    - [SynthesizeResponse](#ondewo.t2s.SynthesizeResponse)
    - [T2SCustomLengthScales](#ondewo.t2s.T2SCustomLengthScales)
    - [T2SDescription](#ondewo.t2s.T2SDescription)
    - [T2SGetServiceInfoResponse](#ondewo.t2s.T2SGetServiceInfoResponse)
    - [T2SInference](#ondewo.t2s.T2SInference)
    - [T2SNormalization](#ondewo.t2s.T2SNormalization)
    - [T2sCloudProviderConfig](#ondewo.t2s.T2sCloudProviderConfig)
    - [T2sCloudProviderConfigElevenLabs](#ondewo.t2s.T2sCloudProviderConfigElevenLabs)
    - [T2sCloudProviderConfigGoogle](#ondewo.t2s.T2sCloudProviderConfigGoogle)
    - [T2sCloudProviderConfigMicrosoft](#ondewo.t2s.T2sCloudProviderConfigMicrosoft)
    - [T2sCloudServiceAmazon](#ondewo.t2s.T2sCloudServiceAmazon)
    - [T2sCloudServiceElevenLabs](#ondewo.t2s.T2sCloudServiceElevenLabs)
    - [T2sCloudServiceGoogle](#ondewo.t2s.T2sCloudServiceGoogle)
    - [T2sCloudServiceMicrosoft](#ondewo.t2s.T2sCloudServiceMicrosoft)
    - [T2sPipelineId](#ondewo.t2s.T2sPipelineId)
    - [Text2Audio](#ondewo.t2s.Text2Audio)
    - [Text2Mel](#ondewo.t2s.Text2Mel)
    - [Text2SpeechConfig](#ondewo.t2s.Text2SpeechConfig)
    - [UpdateCustomPhonemizerRequest](#ondewo.t2s.UpdateCustomPhonemizerRequest)
    - [Vits](#ondewo.t2s.Vits)
    - [VitsTriton](#ondewo.t2s.VitsTriton)
    - [VoiceSettings](#ondewo.t2s.VoiceSettings)
    - [Wiener](#ondewo.t2s.Wiener)
  
    - [AudioFormat](#ondewo.t2s.AudioFormat)
    - [Pcm](#ondewo.t2s.Pcm)
    - [UpdateCustomPhonemizerRequest.UpdateMethod](#ondewo.t2s.UpdateCustomPhonemizerRequest.UpdateMethod)
  
    - [Text2Speech](#ondewo.t2s.Text2Speech)
  
- [Scalar Value Types](#scalar-value-types)



<a name="ondewo/t2s/text-to-speech.proto"></a>
<p align="right"><a href="#top">Top</a></p>

## ondewo/t2s/text-to-speech.proto



<a name="ondewo.t2s.Apodization"></a>

### Apodization
Apodization message contains settings for apodization postprocessing.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| apodization_secs | [float](#float) |  | The duration of apodization in seconds. |






<a name="ondewo.t2s.BatchSynthesizeRequest"></a>

### BatchSynthesizeRequest
BatchSynthesizeRequest message is used to send a batch request for synthesis.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| batch_request | [SynthesizeRequest](#ondewo.t2s.SynthesizeRequest) | repeated | Repeated field holding individual synthesis requests that make up the batch request. |






<a name="ondewo.t2s.BatchSynthesizeResponse"></a>

### BatchSynthesizeResponse
BatchSynthesizeResponse message is used to store the responses for a batch synthesis request.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| batch_response | [SynthesizeResponse](#ondewo.t2s.SynthesizeResponse) | repeated | Repeated field holding individual synthesis responses that correspond to the input requests in the batch. |






<a name="ondewo.t2s.Caching"></a>

### Caching
Caching message contains settings for caching.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| active | [bool](#bool) |  | Flag indicating whether caching is active. |
| memory_cache_max_size | [int64](#int64) |  | The maximum size of the memory cache. |
| sampling_rate | [int64](#int64) |  | The sampling rate for caching. |
| load_cache | [bool](#bool) |  | Flag indicating whether to load cache. |
| save_cache | [bool](#bool) |  | Flag indicating whether to save cache. |
| cache_save_dir | [string](#string) |  | The directory path to save the cache. |






<a name="ondewo.t2s.CompositeInference"></a>

### CompositeInference
CompositeInference message combines text-to-mel and mel-to-audio inference settings.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| text2mel | [Text2Mel](#ondewo.t2s.Text2Mel) |  | Text-to-mel inference settings. |
| mel2audio | [Mel2Audio](#ondewo.t2s.Mel2Audio) |  | Mel-to-audio inference settings. |






<a name="ondewo.t2s.CreateCustomPhonemizerRequest"></a>

### CreateCustomPhonemizerRequest
CreateCustomPhonemizerRequest message represents the request for creating a custom phonemizer.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| prefix | [string](#string) |  | The prefix for the custom phonemizer ID. |
| maps | [Map](#ondewo.t2s.Map) | repeated | Repeated field of Map messages representing word-to-phoneme mappings. |






<a name="ondewo.t2s.CustomPhonemizerProto"></a>

### CustomPhonemizerProto
CustomPhonemizerProto message represents a custom phonemizer.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| id | [string](#string) |  | The ID of the custom phonemizer. |
| maps | [Map](#ondewo.t2s.Map) | repeated | Repeated field of Map messages representing word-to-phoneme mappings. |






<a name="ondewo.t2s.GlowTTS"></a>

### GlowTTS
GlowTTS message contains settings for the GlowTTS inference.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| batch_size | [int64](#int64) |  | The batch size for inference. |
| use_gpu | [bool](#bool) |  | Flag indicating whether to use GPU for inference. |
| length_scale | [float](#float) |  | The length scale for inference. |
| noise_scale | [float](#float) |  | The noise scale for inference. |
| path | [string](#string) |  | The path to the GlowTTS model. |
| cleaners | [string](#string) | repeated | Repeated field containing the cleaners for text normalization. |
| param_config_path | [string](#string) |  | The path to the parameter configuration. |






<a name="ondewo.t2s.GlowTTSTriton"></a>

### GlowTTSTriton
GlowTTSTriton message contains settings for the GlowTTS Triton inference.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| batch_size | [int64](#int64) |  | The batch size for inference. |
| length_scale | [float](#float) |  | The length scale for inference. |
| noise_scale | [float](#float) |  | The noise scale for inference. |
| cleaners | [string](#string) | repeated | Repeated field containing the cleaners for text normalization. |
| max_text_length | [int64](#int64) |  | The maximum text length allowed. |
| param_config_path | [string](#string) |  | The path to the parameter configuration. |
| triton_model_name | [string](#string) |  | The name of the Triton model. |
| triton_server_host | [string](#string) |  | The host of the Triton inference server which servers the model. |
| triton_server_port | [int64](#int64) |  | The port of the Triton inference server which servers the model. |






<a name="ondewo.t2s.HiFiGan"></a>

### HiFiGan
HiFiGan message contains settings for the HiFiGan inference.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| use_gpu | [bool](#bool) |  | Flag indicating whether to use GPU for inference. |
| batch_size | [int64](#int64) |  | The batch size for inference. |
| config_path | [string](#string) |  | The path to the HiFiGan configuration. |
| model_path | [string](#string) |  | The path to the HiFiGan model. |






<a name="ondewo.t2s.HiFiGanTriton"></a>

### HiFiGanTriton
HiFiGanTriton message contains settings for the HiFiGan Triton inference.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| config_path | [string](#string) |  | The path to the HiFiGan Triton configuration. |
| triton_model_name | [string](#string) |  | The name of the Triton model. |
| triton_server_host | [string](#string) |  | The host of the Triton inference server which servers the model. |
| triton_server_port | [int64](#int64) |  | The port of the Triton inference server which servers the model. |






<a name="ondewo.t2s.ListCustomPhonemizerRequest"></a>

### ListCustomPhonemizerRequest
ListCustomPhonemizerRequest message represents the request for listing custom phonemizers.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| pipeline_ids | [string](#string) | repeated | Repeated field of pipeline IDs to filter the list of custom phonemizers. |






<a name="ondewo.t2s.ListCustomPhonemizerResponse"></a>

### ListCustomPhonemizerResponse
ListCustomPhonemizerResponse message represents the response for listing custom phonemizers.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| phonemizers | [CustomPhonemizerProto](#ondewo.t2s.CustomPhonemizerProto) | repeated | Repeated field of CustomPhonemizerProto messages representing the custom phonemizers. |






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






<a name="ondewo.t2s.ListT2sNormalizationPipelinesRequest"></a>

### ListT2sNormalizationPipelinesRequest
The request message for ListT2sNormalizationPipelines.
Filter pipelines by attributed in request.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| language | [string](#string) |  | Optional. Define the language. |






<a name="ondewo.t2s.ListT2sNormalizationPipelinesResponse"></a>

### ListT2sNormalizationPipelinesResponse
Pipeline Response representation.
The response message for ListT2sNormalizationPipelines.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| t2s_normalization_pipelines | [string](#string) | repeated | Required. Representation of a list of normalization pipelines configurations. Retrieved by ListT2sNormalizationPipelines, containing the configurations of normalization pipelines with the specifications received in the ListT2sNormalizationPipelinesRequest. |






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
Logmnse message contains settings for Logmnse postprocessing.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| initial_noise | [int64](#int64) |  | The initial noise value. |
| window_size | [int64](#int64) |  | The window size. |
| noise_threshold | [float](#float) |  | The noise threshold. |






<a name="ondewo.t2s.Map"></a>

### Map
Map message represents a word-to-phoneme mapping in a custom phonemizer.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| word | [string](#string) |  | The word to be mapped. |
| phoneme_groups | [string](#string) |  | The phoneme groups associated with the word. |






<a name="ondewo.t2s.MbMelganTriton"></a>

### MbMelganTriton
MbMelganTriton message contains settings for the MbMelgan Triton inference.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| config_path | [string](#string) |  | The path to the MbMelgan Triton configuration. |
| stats_path | [string](#string) |  | The path to the MbMelgan statistics. |
| triton_model_name | [string](#string) |  | The name of the Triton model. |
| triton_server_host | [string](#string) |  | The host of the Triton inference server which servers the model. |
| triton_server_port | [int64](#int64) |  | The port of the Triton inference server which servers the model. |






<a name="ondewo.t2s.Mel2Audio"></a>

### Mel2Audio
Mel2Audio message contains settings for mel-to-audio inference.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| type | [string](#string) |  | The type of mel-to-audio inference. |
| mb_melgan_triton | [MbMelganTriton](#ondewo.t2s.MbMelganTriton) |  | MbMelgan Triton inference settings. |
| hifi_gan | [HiFiGan](#ondewo.t2s.HiFiGan) |  | HiFiGan inference settings. |
| hifi_gan_triton | [HiFiGanTriton](#ondewo.t2s.HiFiGanTriton) |  | HiFiGan Triton inference settings. |






<a name="ondewo.t2s.NormalizeTextRequest"></a>

### NormalizeTextRequest
NormalizeTextRequest message is used to request text normalization.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| t2s_pipeline_id | [string](#string) |  | The ID of the text-to-speech pipeline. |
| text | [string](#string) |  | The text to be normalized. |






<a name="ondewo.t2s.NormalizeTextResponse"></a>

### NormalizeTextResponse
NormalizeTextResponse message is used to store the normalized text response.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| normalized_text | [string](#string) |  | The normalized text. |






<a name="ondewo.t2s.PhonemizerId"></a>

### PhonemizerId
PhonemizerId message represents the ID of a phonemizer.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| id | [string](#string) |  | The ID of the phonemizer. |






<a name="ondewo.t2s.Postprocessing"></a>

### Postprocessing
Postprocessing message contains settings for postprocessing.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| silence_secs | [float](#float) |  | The duration of silence in seconds. |
| pipeline | [string](#string) | repeated | Repeated field containing pipeline names. |
| logmmse | [Logmnse](#ondewo.t2s.Logmnse) |  | Logmnse postprocessing settings. |
| wiener | [Wiener](#ondewo.t2s.Wiener) |  | Wiener postprocessing settings. |
| apodization | [Apodization](#ondewo.t2s.Apodization) |  | Apodization postprocessing settings. |






<a name="ondewo.t2s.RequestConfig"></a>

### RequestConfig
Represents a Configuration for the text to speech conversion.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| t2s_pipeline_id | [string](#string) |  | Required. Represents the pipeline id of the model configuration that will be used. |
| length_scale | [float](#float) |  | Optional. This parameter is used for time stretching which is the process of changing the speed or duration of an audio. It should be much more than 1.0. O is not a valid number for this variable. The default value is 1. |
| noise_scale | [float](#float) |  | Optional. Defines the noise in the generated audio. It should be between 0.0 and 1. The default value is 0.0 |
| sample_rate | [int32](#int32) |  | Optional. Defines the sample rate of the generated wav file. The default value is 22050. |
| pcm | [Pcm](#ondewo.t2s.Pcm) |  | Optional. Defines the pulse-code modulation of the wav file. The default value is PCM_16. |
| audio_format | [AudioFormat](#ondewo.t2s.AudioFormat) |  | Optional. Defines the format of the desired audio. The default value is wav. |
| use_cache | [bool](#bool) |  | Optional. Define if cache should be used or not. The default value is False. |
| t2s_service_config | [google.protobuf.Struct](#google.protobuf.Struct) | optional | Optional. t2s_service_config provides the configuration of the service such as API key, bearer tokens, JWT, and other header information as key value pairs, e.g., <pre><code>MY_API_KEY='LKJDIFe244LKJOI'</code></pre> A. For Amazon T2S service, the following arguments should be passed: A1. aws_access_key_id (required) Access key id to access Amazon WEB Service. A2. aws_secret_access_key (required) Secret access key to access Amazon WEB Service. A3. region (required) Region name of Amazon Server. Example: t2s_config_service={'aws_access_key_id': 'YOUR_AWS_ACCESS_KEY_ID', 'aws_secret_access_key': 'YOUR_AWS_SECRET_ACCESS_KEY', 'region': 'YOUR_AMAZON_SERVER_REGION_NAME'} B. For ElevenLabs T2s service, the following arguments should be passed: B1. api_key (required) API key of ElevenLabs cloud provider to access its T2S service. Example: t2s_config_service={'api_key': 'YOUR_ELEVENLABS_API_KEY'} C. For Google cloud T2S service, the following arguments should be passed: C1. api_key (required) API key of Google cloud provider to access its T2S service. C2. api_endpoint (optional) Regional API endpoint of Google cloud T2S service. (Defaults to 'eu-texttospeech.googleapis.com') Example: t2s_config_service={'api_key': 'YOUR_GOOGLE_CLOUD_API_KEY', 'api_endpoint': 'YOUR_GOOGLE_CLOUD_API_ENDPOINT'} D. For Microsoft Azure T2s service, the following arguments should be passed: D1. subscription_key (required) Subscription key to access Microsoft Azure Service. D2. region (required) Region name of Microsoft Azure Server. Example: t2s_config_service={'subscription_key': 'YOUR_MICROSOFT_AZURE_SUBSCRIPTION_KEY', 'region': 'YOUR_MICROSOFT_AZURE_SERVER_REGION_NAME'} Note: ondewo-t2s will raise an error if you don't pass any of the required arguments above. |
| t2s_cloud_provider_config | [T2sCloudProviderConfig](#ondewo.t2s.T2sCloudProviderConfig) | optional | Optional. Defines the cloud provider's specific configuration for using text to speech cloud services The default value is None. |
| t2s_normalization | [T2SNormalization](#ondewo.t2s.T2SNormalization) |  | Optional. Define t2s_normalization config parameters for this specific request. The default values are set in the config file and the values set via RequestConfig are set just for this specific request and will not update the pipeline. |
| word_to_phoneme_mapping | [google.protobuf.Struct](#google.protobuf.Struct) | optional | Optional. Define a dict which specifies the phonemes for a special word. |






<a name="ondewo.t2s.SingleInference"></a>

### SingleInference
SingleInference message inference settings of text2audio models.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| text2audio | [Text2Audio](#ondewo.t2s.Text2Audio) |  | Text-to-audio inference settings. |






<a name="ondewo.t2s.StreamingSynthesizeRequest"></a>

### StreamingSynthesizeRequest
StreamingSynthesizeRequest is used to perform streaming synthesize.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| text | [string](#string) |  | Required. Represents the text that will be transformed to speech. All the properties according to the input text in SynthesizeRequest can be also applied here. |
| config | [RequestConfig](#ondewo.t2s.RequestConfig) |  | Required. Represents the specifications needed to do the text to speech transformation. |






<a name="ondewo.t2s.StreamingSynthesizeResponse"></a>

### StreamingSynthesizeResponse
Represents a Streaming Synthesize Response.
A Streaming Synthesize Response contains the generated audio, requested text and and
all other properties of this generated audio.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| audio_uuid | [string](#string) |  | Required. Represents the pipeline id of the model configuration that will be used. |
| audio | [bytes](#bytes) |  | Required. Generated file with the parameters described in request. |
| generation_time | [float](#float) |  | Required. Time to generate audio. |
| audio_length | [float](#float) |  | Required. Audio length. |
| text | [string](#string) |  | Required. Text from which audio was generated. |
| config | [RequestConfig](#ondewo.t2s.RequestConfig) |  | Required. Configuration from which audio was generated. |
| normalized_text | [string](#string) |  | Optional. Normalized text. |
| sample_rate | [float](#float) |  | Optional. Value of sampling rate |






<a name="ondewo.t2s.SynthesizeRequest"></a>

### SynthesizeRequest
Represents a Synthesize Request.
A Synthesize Request contains the information need to perform a text to speech conversion.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| text | [string](#string) |  | Required. Represents the text that will be transformed to speech.

<p> Synthesize text: </p>

- Simple text: <pre><code>Hello, how are you?</code></pre>

<p>Examples to modulate the voice based on SSML tags and Arpabet phonemes:</p>

- SSML Tag Phone: <pre><code>&lt;say-as interpret-as="phone">+12354321&lt;/say-as&gt;</code></pre>

- SSML Tag Email: <pre><code>&lt;say-as interpret-as="email">voices@ondewo.com&lt;/say-as&gt;</code></pre>

- SSML Tag URL: <pre><code>&lt;say-as interpret-as="url">ondewo.com/en/&lt;/say-as&gt;</code></pre>

- SSML Tag Spell: <pre><code>&lt;say-as interpret-as="spell">AP732&lt;/say-as&gt;</code></pre>

- SSML Tag Spell With Names: <pre><code>&lt;say-as interpret-as="spell-with-names">AHO32&lt;/say-as&gt;</code></pre>

- SSML Tag Callsigns Short: <pre><code>&lt;say-as interpret-as="callsign-short">AUA439&lt;/say-as&gt;</code></pre>

- SSML Tag Callsigns Long: <pre><code>&lt;say-as interpret-as="callsign-long">AAL439&lt;/say-as&gt;</code></pre>

- SSML Tag Break Tag: <pre><code>I am going to take a 2 seconds break <break time="2.0"/> done</code></pre>

- Arpabet Phonemes: <pre><code>Hello I am {AE2 L EH0 G Z AE1 N D R AH0}</code></pre> |
| config | [RequestConfig](#ondewo.t2s.RequestConfig) |  | Required. Represents the specifications needed to do the text to speech transformation. |






<a name="ondewo.t2s.SynthesizeResponse"></a>

### SynthesizeResponse
Represents a Synthesize Response.
A Synthesize Response contains the generated audio, requested text and all other properties of this generated audio.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| audio_uuid | [string](#string) |  | Required. Represents the pipeline id of the model configuration that will be used. |
| audio | [bytes](#bytes) |  | Required. Generated file with the parameters described in request. |
| generation_time | [float](#float) |  | Required. Time to generate audio. |
| audio_length | [float](#float) |  | Required. Audio length. |
| text | [string](#string) |  | Required. Text from which audio was generated. |
| config | [RequestConfig](#ondewo.t2s.RequestConfig) |  | Required. Configuration from which audio was generated. |
| normalized_text | [string](#string) |  | Optional. Normalized text. |
| sample_rate | [float](#float) |  | Optional. Value of sampling rate |






<a name="ondewo.t2s.T2SCustomLengthScales"></a>

### T2SCustomLengthScales
T2SCustomLengthScales message contains custom length scales for text types.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| text | [float](#float) |  | The custom length scale for general text. |
| email | [float](#float) |  | The custom length scale for email text. |
| url | [float](#float) |  | The custom length scale for URL text. |
| phone | [float](#float) |  | The custom length scale for phone number text. |
| spell | [float](#float) |  | The custom length scale for spelled-out text. |
| spell_with_names | [float](#float) |  | The custom length scale for spelled-out text with names. |
| callsign_long | [float](#float) |  | The custom length scale for long callsigns. |
| callsign_short | [float](#float) |  | The custom length scale for short callsigns. |






<a name="ondewo.t2s.T2SDescription"></a>

### T2SDescription
T2SDescription message is used to describe the text-to-speech service.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| language | [string](#string) |  | The language supported by the service. |
| speaker_sex | [string](#string) |  |  |
| pipeline_owner | [string](#string) |  | The owner of the text-to-speech pipeline. |
| comments | [string](#string) |  | Additional comments or notes. |
| speaker_name | [string](#string) |  | The name of the speaker. |
| domain | [string](#string) |  | The domain or context of the service. |






<a name="ondewo.t2s.T2SGetServiceInfoResponse"></a>

### T2SGetServiceInfoResponse
Version information of the service


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| version | [string](#string) |  | version number |






<a name="ondewo.t2s.T2SInference"></a>

### T2SInference
T2SInference message is used to specify the text-to-speech inference settings.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| type | [string](#string) |  | The type of inference. |
| composite_inference | [CompositeInference](#ondewo.t2s.CompositeInference) |  | Composite inference settings. |
| single_inference | [SingleInference](#ondewo.t2s.SingleInference) |  | Single inference settings. |
| caching | [Caching](#ondewo.t2s.Caching) |  | Caching settings. |






<a name="ondewo.t2s.T2SNormalization"></a>

### T2SNormalization
Represents the configuration for text-to-speech normalization.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| language | [string](#string) |  | The language for which the normalization is applied. |
| pipeline | [string](#string) | repeated | The pipeline(s) used for normalization. |
| custom_phonemizer_id | [string](#string) |  | The ID of the custom phonemizer, if used. |
| custom_length_scales | [T2SCustomLengthScales](#ondewo.t2s.T2SCustomLengthScales) |  | Custom length scales for different text types. |
| arpabet_mapping | [string](#string) |  | The mapping for Arpabet phonemes. |
| numeric_mapping | [string](#string) |  | The mapping for numeric expressions. |
| callsigns_mapping | [string](#string) |  | The mapping for callsigns. |
| phoneme_correction_mapping | [string](#string) |  | The mapping for phoneme correction. |






<a name="ondewo.t2s.T2sCloudProviderConfig"></a>

### T2sCloudProviderConfig
Configuration for cloud provider settings for Text-to-Speech (T2S).


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| t2s_cloud_provider_config_elevenlabs | [T2sCloudProviderConfigElevenLabs](#ondewo.t2s.T2sCloudProviderConfigElevenLabs) |  | Configuration for Eleven Labs text-to-speech provider. |
| t2s_cloud_provider_config_google | [T2sCloudProviderConfigGoogle](#ondewo.t2s.T2sCloudProviderConfigGoogle) |  | Configuration for Google text-to-speech provider. |
| t2s_cloud_provider_config_microsoft | [T2sCloudProviderConfigMicrosoft](#ondewo.t2s.T2sCloudProviderConfigMicrosoft) |  | Configuration for Microsoft text-to-speech provider. |






<a name="ondewo.t2s.T2sCloudProviderConfigElevenLabs"></a>

### T2sCloudProviderConfigElevenLabs
Configuration details specific to the Eleven Labs text-to-speech provider.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| stability | [float](#float) |  | Stability level for inference, influencing consistency of generated speech. It is in the range [0.0, 1.0]. |
| similarity_boost | [float](#float) |  | Boost value for similarity to enhance the similarity of the generated voice to a target voice. It is in the range [0.0, 1.0]. |
| style | [float](#float) |  | Style parameter to control the expression or emotion in speech. It is in the range [0.0, 1.0]. |
| use_speaker_boost | [bool](#bool) |  | Enables or disables speaker boost for emphasis on clarity and loudness. |
| apply_text_normalization | [string](#string) |  | Specifies type of text normalization to apply during processing. Available options are 'auto', 'on', and 'off'. |






<a name="ondewo.t2s.T2sCloudProviderConfigGoogle"></a>

### T2sCloudProviderConfigGoogle
Configuration details specific to the Google text-to-speech provider.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| speaking_rate | [float](#float) |  | Speaking rate for inference, controlling the speed of generated speech. It is in the range [0.25, 4.0]. |
| volume_gain_db | [float](#float) |  | Volume gain in dB applied to the generated speech. It is in the range [-96.0, 16.0]. |
| pitch | [float](#float) |  | Pitch adjustment for inference, allowing control over voice pitch. It is in the range in the range [-20.0, 20.0]. |






<a name="ondewo.t2s.T2sCloudProviderConfigMicrosoft"></a>

### T2sCloudProviderConfigMicrosoft
Configuration details specific to the Microsoft text-to-speech provider.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| use_default_speaker | [bool](#bool) |  | Determines whether to use the default speaker voice. |






<a name="ondewo.t2s.T2sCloudServiceAmazon"></a>

### T2sCloudServiceAmazon
T2sCloudServiceAmazon message contains settings for the Amazon Cloud service inference.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| voice_id | [string](#string) |  | Voice ID indicating the speaker |
| model_id | [string](#string) |  | Model id for the inference server. |






<a name="ondewo.t2s.T2sCloudServiceElevenLabs"></a>

### T2sCloudServiceElevenLabs
T2sCloudServiceElevenLabs message contains settings for the ElevenLabs Cloud service inference.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| language_code | [string](#string) |  | Language of the generated audio. It should be 4-Letter language code. |
| model_id | [string](#string) |  | Model ID indicating the name of the model |
| voice_id | [string](#string) |  | Voice ID indicating the speaker |
| voice_settings | [VoiceSettings](#ondewo.t2s.VoiceSettings) |  | Voice setting of the inference |
| apply_text_normalization | [string](#string) |  | Flag to indicate applying text normalization |






<a name="ondewo.t2s.T2sCloudServiceGoogle"></a>

### T2sCloudServiceGoogle
T2sCloudServiceGoogle message contains settings for the Google Cloud service inference.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| voice_id | [string](#string) |  | Voice ID indicating the speaker |
| speaking_rate | [float](#float) |  | Speaking rate to control the speed of audio. |
| volume_gain_db | [float](#float) |  | Volume gain in db to control volume of the audio. |
| pitch | [float](#float) |  | pitch value of the audio |






<a name="ondewo.t2s.T2sCloudServiceMicrosoft"></a>

### T2sCloudServiceMicrosoft
T2sCloudServiceMicrosoft message contains settings for the Microsoft Cloud service inference.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| voice_id | [string](#string) |  | Voice ID indicating the speaker. |
| use_default_speaker | [bool](#bool) |  | Flag to indicate using the default speaker. |






<a name="ondewo.t2s.T2sPipelineId"></a>

### T2sPipelineId
Pipeline Id representation.
Used in the creation, deletion and getter of pipelines.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| id | [string](#string) |  | Required. Defines the id of the pipeline. |






<a name="ondewo.t2s.Text2Audio"></a>

### Text2Audio
Text2Audio message contains settings for text-to-audio inference.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| type | [string](#string) |  | The type of text-to-audio inference. |
| vits | [Vits](#ondewo.t2s.Vits) |  | Vits inference settings. |
| vits_triton | [VitsTriton](#ondewo.t2s.VitsTriton) |  | Vits Triton inference settings. |
| t2s_cloud_service_elevenlabs | [T2sCloudServiceElevenLabs](#ondewo.t2s.T2sCloudServiceElevenLabs) |  | ElevenLabs cloud service inference settings. |
| t2s_cloud_service_amazon | [T2sCloudServiceAmazon](#ondewo.t2s.T2sCloudServiceAmazon) |  | Amazon cloud service inference settings. |
| t2s_cloud_service_google | [T2sCloudServiceGoogle](#ondewo.t2s.T2sCloudServiceGoogle) |  | Google cloud service inference settings. |
| t2s_cloud_service_microsoft | [T2sCloudServiceMicrosoft](#ondewo.t2s.T2sCloudServiceMicrosoft) |  | Microsoft cloud service inference settings. |






<a name="ondewo.t2s.Text2Mel"></a>

### Text2Mel
Text2Mel message contains settings for text-to-mel inference.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| type | [string](#string) |  | The type of text-to-mel inference. |
| glow_tts | [GlowTTS](#ondewo.t2s.GlowTTS) |  | GlowTTS inference settings. |
| glow_tts_triton | [GlowTTSTriton](#ondewo.t2s.GlowTTSTriton) |  | GlowTTS Triton inference settings. |






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
UpdateCustomPhonemizerRequest message represents the request for updating a custom phonemizer.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| id | [string](#string) |  | The ID of the custom phonemizer to be updated. |
| update_method | [UpdateCustomPhonemizerRequest.UpdateMethod](#ondewo.t2s.UpdateCustomPhonemizerRequest.UpdateMethod) |  | The update method. |
| maps | [Map](#ondewo.t2s.Map) | repeated | Repeated field of Map messages representing word-to-phoneme mappings. |






<a name="ondewo.t2s.Vits"></a>

### Vits



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| batch_size | [int64](#int64) |  | The batch size for inference. |
| use_gpu | [bool](#bool) |  | Flag indicating whether to use GPU for inference. |
| length_scale | [float](#float) |  | The length scale for inference. |
| noise_scale | [float](#float) |  | The noise scale for inference. |
| path | [string](#string) |  | The path to the Vits model. |
| cleaners | [string](#string) | repeated | Repeated field containing the cleaners for text normalization. |
| param_config_path | [string](#string) |  | The path to the parameter configuration. |






<a name="ondewo.t2s.VitsTriton"></a>

### VitsTriton
VitsTriton message contains settings for the Vits Triton inference.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| batch_size | [int64](#int64) |  | The batch size for inference. |
| length_scale | [float](#float) |  | The length scale for inference. |
| noise_scale | [float](#float) |  | The noise scale for inference. |
| cleaners | [string](#string) | repeated | Repeated field containing the cleaners for text normalization. |
| max_text_length | [int64](#int64) |  | The maximum text length allowed. |
| param_config_path | [string](#string) |  | The path to the parameter configuration. |
| triton_model_name | [string](#string) |  | The name of the Triton model. |
| triton_server_host | [string](#string) |  | The host of the Triton inference server which servers the model. |
| triton_server_port | [int64](#int64) |  | The port of the Triton inference server which servers the model. |






<a name="ondewo.t2s.VoiceSettings"></a>

### VoiceSettings
VoiceSettings message contains settings for ElevenLabs inference.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| stability | [float](#float) |  | stability value for elevenlabs inference |
| similarity_boost | [float](#float) |  | similarity boost value for ElevenLabs inference. |
| style | [float](#float) |  | style boost value for ElevenLabs inference. |
| use_speaker_boost | [bool](#bool) |  | Flag to indicate speaker boost |






<a name="ondewo.t2s.Wiener"></a>

### Wiener
Wiener message contains settings for Wiener postprocessing.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| frame_len | [int64](#int64) |  | The frame length. |
| lpc_order | [int64](#int64) |  | The LPC order. |
| iterations | [int64](#int64) |  | The number of iterations. |
| alpha | [float](#float) |  | The alpha value. |
| thresh | [float](#float) |  | The threshold value. |





 <!-- end messages -->


<a name="ondewo.t2s.AudioFormat"></a>

### AudioFormat
AudioFormat enum represents various audio file formats for storing digital audio data.

| Name | Number | Description |
| ---- | ------ | ----------- |
| wav | 0 | Waveform Audio File Format (WAV) |
| flac | 1 | Free Lossless Audio Codec (FLAC) |
| caf | 2 | Core Audio Format (CAF) |
| mp3 | 3 | MPEG Audio Layer III (MP3) |
| aac | 4 | Advanced Audio Coding (AAC) |
| ogg | 5 | Ogg Vorbis (OGG) |
| wma | 6 | Windows Media Audio (WMA) |



<a name="ondewo.t2s.Pcm"></a>

### Pcm
Represents a pulse-code modulation technique.

| Name | Number | Description |
| ---- | ------ | ----------- |
| PCM_16 | 0 | 16-bit pulse-code modulation. |
| PCM_24 | 1 | 24-bit pulse-code modulation. |
| PCM_32 | 2 | 32-bit pulse-code modulation. |
| PCM_S8 | 3 | Signed 8-bit pulse-code modulation. |
| PCM_U8 | 4 | Unsigned 8-bit pulse-code modulation. |
| FLOAT | 5 | Floating-point (32-bit) pulse-code modulation. |
| DOUBLE | 6 | Floating-point (64-bit) pulse-code modulation. |



<a name="ondewo.t2s.UpdateCustomPhonemizerRequest.UpdateMethod"></a>

### UpdateCustomPhonemizerRequest.UpdateMethod
The update method to be used.

| Name | Number | Description |
| ---- | ------ | ----------- |
| extend_hard | 0 | Add new words, replacing existing ones. |
| extend_soft | 1 | Add new words if they are not already present. |
| replace | 2 | Replace all words in the phonemizer with new ones. |


 <!-- end enums -->

 <!-- end HasExtensions -->


<a name="ondewo.t2s.Text2Speech"></a>

### Text2Speech
Text2Speech service provides endpoints for text-to-speech generation.

| Method Name | Request Type | Response Type | Description |
| ----------- | ------------ | ------------- | ------------|
| Synthesize | [SynthesizeRequest](#ondewo.t2s.SynthesizeRequest) | [SynthesizeResponse](#ondewo.t2s.SynthesizeResponse) | Synthesize RPC

Synthesizes a specific text sent in the request with the provided configuration requirements and retrieves a response that includes the synthesized text as audio and the requested configuration. |
| BatchSynthesize | [BatchSynthesizeRequest](#ondewo.t2s.BatchSynthesizeRequest) | [BatchSynthesizeResponse](#ondewo.t2s.BatchSynthesizeResponse) | BatchSynthesize RPC

Performs batch synthesis by accepting a batch of synthesis requests and returning a batch response. This can be more efficient for generating predictions on the AI model in bulk. |
| StreamingSynthesize | [StreamingSynthesizeRequest](#ondewo.t2s.StreamingSynthesizeRequest) stream | [StreamingSynthesizeResponse](#ondewo.t2s.StreamingSynthesizeResponse) stream | Performs streaming synthesis by accepting stream of input text and returning a stream of generated audio. |
| NormalizeText | [NormalizeTextRequest](#ondewo.t2s.NormalizeTextRequest) | [NormalizeTextResponse](#ondewo.t2s.NormalizeTextResponse) | NormalizeText RPC

Normalizes a text according to the specific pipeline's normalization rules. |
| GetT2sPipeline | [T2sPipelineId](#ondewo.t2s.T2sPipelineId) | [Text2SpeechConfig](#ondewo.t2s.Text2SpeechConfig) | GetT2sPipeline RPC

Retrieves the configuration of the specified text-to-speech pipeline. |
| CreateT2sPipeline | [Text2SpeechConfig](#ondewo.t2s.Text2SpeechConfig) | [T2sPipelineId](#ondewo.t2s.T2sPipelineId) | CreateT2sPipeline RPC

Creates a new text-to-speech pipeline with the provided configuration and returns its pipeline ID. |
| DeleteT2sPipeline | [T2sPipelineId](#ondewo.t2s.T2sPipelineId) | [.google.protobuf.Empty](#google.protobuf.Empty) | DeleteT2sPipeline RPC

Deletes the specified text-to-speech pipeline. |
| UpdateT2sPipeline | [Text2SpeechConfig](#ondewo.t2s.Text2SpeechConfig) | [.google.protobuf.Empty](#google.protobuf.Empty) | UpdateT2sPipeline RPC

Updates the specified text-to-speech pipeline with the given configuration. |
| ListT2sPipelines | [ListT2sPipelinesRequest](#ondewo.t2s.ListT2sPipelinesRequest) | [ListT2sPipelinesResponse](#ondewo.t2s.ListT2sPipelinesResponse) | ListT2sPipelines RPC

Retrieves a list of text-to-speech pipelines based on specific requirements. |
| ListT2sLanguages | [ListT2sLanguagesRequest](#ondewo.t2s.ListT2sLanguagesRequest) | [ListT2sLanguagesResponse](#ondewo.t2s.ListT2sLanguagesResponse) | ListT2sLanguages RPC

Retrieves a list of languages available based on specific configuration requirements. |
| ListT2sDomains | [ListT2sDomainsRequest](#ondewo.t2s.ListT2sDomainsRequest) | [ListT2sDomainsResponse](#ondewo.t2s.ListT2sDomainsResponse) | ListT2sDomains RPC

Retrieves a list of domains available based on specific configuration requirements. |
| ListT2sNormalizationPipelines | [ListT2sNormalizationPipelinesRequest](#ondewo.t2s.ListT2sNormalizationPipelinesRequest) | [ListT2sNormalizationPipelinesResponse](#ondewo.t2s.ListT2sNormalizationPipelinesResponse) | ListT2sNormalizationPipelines RPC

Retrieves a list of normalization pipelines based on specific requirements. |
| GetServiceInfo | [.google.protobuf.Empty](#google.protobuf.Empty) | [T2SGetServiceInfoResponse](#ondewo.t2s.T2SGetServiceInfoResponse) | GetServiceInfo RPC

Retrieves the version information of the running text-to-speech server. |
| GetCustomPhonemizer | [PhonemizerId](#ondewo.t2s.PhonemizerId) | [CustomPhonemizerProto](#ondewo.t2s.CustomPhonemizerProto) | GetCustomPhonemizer RPC

Retrieves a custom phonemizer based on the provided PhonemizerId. |
| CreateCustomPhonemizer | [CreateCustomPhonemizerRequest](#ondewo.t2s.CreateCustomPhonemizerRequest) | [PhonemizerId](#ondewo.t2s.PhonemizerId) | CreateCustomPhonemizer RPC

Creates a custom phonemizer based on the provided CreateCustomPhonemizerRequest. Returns the PhonemizerId associated with the created custom phonemizer. |
| DeleteCustomPhonemizer | [PhonemizerId](#ondewo.t2s.PhonemizerId) | [.google.protobuf.Empty](#google.protobuf.Empty) | DeleteCustomPhonemizer RPC

Deletes a custom phonemizer based on the provided PhonemizerId. Returns an Empty response upon successful deletion. |
| UpdateCustomPhonemizer | [UpdateCustomPhonemizerRequest](#ondewo.t2s.UpdateCustomPhonemizerRequest) | [CustomPhonemizerProto](#ondewo.t2s.CustomPhonemizerProto) | UpdateCustomPhonemizer RPC

Updates the specified custom phonemizer with the provided configuration. |
| ListCustomPhonemizer | [ListCustomPhonemizerRequest](#ondewo.t2s.ListCustomPhonemizerRequest) | [ListCustomPhonemizerResponse](#ondewo.t2s.ListCustomPhonemizerResponse) | ListCustomPhonemizer RPC

Retrieves a list of custom phonemizers based on specific requirements. |

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
