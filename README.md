## SmartMirror

Intro to project.

## Code Example


## Motivation

Done as a university project.

## Installation

<p>Clone or Download the <a href="https://github.com/FBOBecker/SmartMirror">Git-Repository</a>.</p>
<p>
Run ’setup.py’  to install the requirements which will give you the required binaries. FILE MUSS NOCH ERSTELLT WERDEN</p>
Visual Output
<p>
The visual output will be displayed as html in a Browser(Chrome by default).
We used selenium for this.
To make sure python can evoke a Browser instance we have to pass an executable to it.
These can be downloaded <a href="http://selenium-python.readthedocs.io/installation.html#drivers">here</a>.
</p>
<p>
You need to specify the path to the directory of your executable.
Setting a Path variable in UNIX
export PATH=$PATH your/path/
</p>

## API Reference

Create accounts for the API-Services we used and replace the placeholders in ‘token.py’
<ul>
  <li>
    <h4>Wit.Ai API</h4>
    <p>
        When creating a new app pass the wit.zip-file when asked for it.
        See this <a href="https://wit.ai/docs/recipes#copyexportversion-my-app">Tutorial</a>.
    </p>
    <p>
        For the API-Key navigate to ‘Settings’ inside your wit.ai app and “FURHTEREXPLANATIONNEEDED”
    </p>
  </li>
  <li>
    <h4>Darksky.net API</h4>
    <p>
        Once you created an Account get your API-KEY <a href="https://darksky.net/dev/account">here</a>.
    </p>
  </li>
  <li>
    <h4>Google Maps Geocoding API</h4>
    <p>
        Once you created an Account get your API-KEY <a href="https://developers.google.com/maps/documentation/geocoding/get-api-key">here</a>.
    </p>
  </li>
</ul>

## Tests


## Contributors



## License

A short snippet describing the license (MIT, Apache, etc.)
