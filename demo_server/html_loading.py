from . import DEMO_URL


def get_audiofile() -> str:
    return AUDIOFILE.format(DEMO_URL)


def get_result(wav_filename: str, time: float) -> str:
    return RESULT.format(wav_filename, time)


AUDIOFILE: str = """
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ONDEWO T2S</title>
    <link rel="icon" type="image/x-icon" href="static/images/favicon.ico">
    <link rel="stylesheet" type="text/css" href="static/css/stylesheet.css">
</head>

<body>
    <div class="header">
        <div class="logo-container inline-block">
            <img id="logo" src="static/images/ondewo.png">
        </div>
        <div class="name inline-block">
            <p>T2S</p>
        </div>
        <div class="model-name-container inline-block">
            <div class="introduction">
                <p>(Text to speech DEMO)</p>
            </div>
        </div>
    </div>
        <form action = "{0}/text2speech_web" method = "POST" enctype = "multipart/form-data">
    <div class="text-area-container">
        <textarea name="text" placeholder="Insert your text here.."></textarea>
    </div>
    <div class="options">
    <div class="language-container inline-block">
        <div class="language-container-header inline-block">
            <p>Voice:</p>
        </div>
        <div class="language-options ">
            <div class="inline-block">
                <input id="radio-1" class="radio-custom inline-block" name="voice"  value="Kerstin" type="radio" checked id="kerstin">
                <label for="radio-1" class="radio-custom-label inline-block de">Kerstin (de)</label>
            </div>
            <div class="inline-block">
                <input id="radio-2" class="radio-custom inline-block" name="voice"  value="Thorsten" type="radio" id="thorsten">
                <label for="radio-2" class="radio-custom-label inline-block de">Thorsten (de)</label>
            </div>
            <div class="inline-block">
                <input id="radio-3" class="radio-custom inline-block" name="voice"  value="Sandra" type="radio" id="sandra">
                <label for="radio-3" class="radio-custom-label inline-block de">Sandra (de)</label>
            </div>
            <div class="inline-block">
                <input id="radio-4" class="radio-custom inline-block" name="voice" value="Linda" type="radio" id="linda">
                <label for="radio-4" class="radio-custom-label inline-block en">Linda (en)</label>
            </div>
        </div>

    </div>
        <input type="submit" class="btn inline-block"/>
    </div>
</form>
</body>

</html>

"""

RESULT: str = """
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ONDEWO T2S</title>
    <link rel="icon" type="image/x-icon" href="static/images/favicon.ico">
    <link rel="stylesheet" type="text/css" href="static/css/stylesheet.css">
</head>

<body>
    <div class="header">
        <div class="logo-container inline-block">
            <img id="logo" src="static/images/ondewo.png">
        </div>
        <div class="name inline-block">
            <p>T2S</p>
        </div>
        <div class="model-name-container inline-block">
            <div class="introduction">
                <p>(Text to speech DEMO)</p>
            </div>
        </div>
    </div>
    <div class="content-wrapper-result">
        <div class="info">
            <div class="result">
                <h2><b>Result:</b></h2>
                <audio controls>
                    <source src="wavs/{0}" type="audio/wav">
                    Your browser does not support the audio element.
                </audio>
            </div><br>
            <div class="time">
                <h2><b>Time: </b></h2>
                <p> {1:.3f} seconds</p>
            </div>
        </div>
        <button class="btn margin-top-0" onclick="window.location.href = 'wavs_as_attachment/{0}';">Download audio</button>
    </div>
</body>
</html>
"""
