RESULT: str = """
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ONDEWO Stella</title>
    <link rel="icon" type="image/x-icon" href="static/images/favicon.ico">
    <link rel="stylesheet" type="text/css" href="static/css/stylesheet.css">
</head>

<body>
    <div class="header">
        <div class="logo-container inline-block">
            <img id="logo" src="static/images/ondewo.png">
        </div>
        <div class="name inline-block">
            <p>T2S Stella</p>
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
                    <source src="wav_file" type="audio/wav">
                    Your browser does not support the audio element.
                </audio>
            </div><br>
            <div class="time">
                <h2><b>Time: </b></h2>
                <p> {0:.3f} seconds</p>
            </div>
        </div>
        <button class="btn margin-top-0" onclick="window.location.href = 'wav_file_attachment';">Download audio</button>
    </div>
</body>
</html>
"""