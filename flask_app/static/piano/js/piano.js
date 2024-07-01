const keys = document.querySelector('.keys');
const pianoTitle = document.querySelector('.piano-title');
const pianoBase = document.querySelector('.piano-base');
const awokenTitle = document.querySelector('.awoken-title');
const keyTypesW = document.querySelectorAll('.key-type-w');
const keyTypesB = document.querySelectorAll('.key-type-b');

/*
JS Objects of all keys in piano
*/
const w1 = document.getElementById('w1');
const w2 = document.getElementById('w2');
const w3 = document.getElementById('w3');
const w4 = document.getElementById('w4');
const w5 = document.getElementById('w5');
const w6 = document.getElementById('w6');
const w7 = document.getElementById('w7');
const w8 = document.getElementById('w8');
const w9 = document.getElementById('w9');
const w10 = document.getElementById('w10');
const b1 = document.getElementById('b1');
const b2 = document.getElementById('b2');
const b3 = document.getElementById('b3');
const b4 = document.getElementById('b4');
const b5 = document.getElementById('b5');
const b6 = document.getElementById('b6');
const b7 = document.getElementById('b7');

/*
Map of key codes to key objects
*/
const keyCodeMap = {65: w1, 83: w2, 68: w3, 70: w4, 71: w5, 72: w6, 74: w7, 75: w8, 76: w9, 186: w10,
                    87: b1, 69: b2, 84: b3, 89: b4, 85: b5, 79: b6, 80: b7};

const sound = {65:"http://carolinegabriel.com/demo/js-keyboard/sounds/040.wav",
            87:"http://carolinegabriel.com/demo/js-keyboard/sounds/041.wav",
            83:"http://carolinegabriel.com/demo/js-keyboard/sounds/042.wav",
            69:"http://carolinegabriel.com/demo/js-keyboard/sounds/043.wav",
            68:"http://carolinegabriel.com/demo/js-keyboard/sounds/044.wav",
            70:"http://carolinegabriel.com/demo/js-keyboard/sounds/045.wav",
            84:"http://carolinegabriel.com/demo/js-keyboard/sounds/046.wav",
            71:"http://carolinegabriel.com/demo/js-keyboard/sounds/047.wav",
            89:"http://carolinegabriel.com/demo/js-keyboard/sounds/048.wav",
            72:"http://carolinegabriel.com/demo/js-keyboard/sounds/049.wav",
            85:"http://carolinegabriel.com/demo/js-keyboard/sounds/050.wav",
            74:"http://carolinegabriel.com/demo/js-keyboard/sounds/051.wav",
            75:"http://carolinegabriel.com/demo/js-keyboard/sounds/052.wav",
            79:"http://carolinegabriel.com/demo/js-keyboard/sounds/053.wav",
            76:"http://carolinegabriel.com/demo/js-keyboard/sounds/054.wav",
            80:"http://carolinegabriel.com/demo/js-keyboard/sounds/055.wav",
            186:"http://carolinegabriel.com/demo/js-keyboard/sounds/056.wav"};

const awokenSound = new Audio("https://orangefreesounds.com/wp-content/uploads/2020/09/Creepy-piano-sound-effect.mp3?_=1");

/*
Event listeners for key presses
*/
document.body.addEventListener('keydown', pressKey);
document.body.addEventListener('keyup', releaseKey);

/*
Event listeners for mouse hover
*/
keys.addEventListener('mouseenter', showKeyTypes);
keys.addEventListener('mouseleave', removeKeyTypes);

// Sequence string to check if "weseeyou" was inputted
let seq = "";
let keysActivated = true;

/*
Called when a key is pressed
e: event
*/
function pressKey(e) {
    if (keyCodeMap.hasOwnProperty(e.which) && keysActivated) {
        let note = new Audio(sound[e.which]);
        keyCodeMap[e.which].style.opacity = 0.8;
        note.play();


        seq = seq + e.key;
        if (seq.includes('weseeyou')) {
            keys.style.display = 'none';
            pianoTitle.style.display = 'none';
            awokenTitle.style.display = 'block';
            pianoBase.style.backgroundImage = "url(/static/piano/images/texture.jpeg)";
            pianoBase.style.backgroundSize = "cover";
            pianoBase.style.backgroundPosition = "center";
            pianoBase.style.animation = "fadeIn ease 2s"

            awokenSound.play();
            keysActivated = false;
            seq = "";
        }
    }

}

/*
Called when a key is released
e: event
*/
function releaseKey(e) {
    if (keyCodeMap.hasOwnProperty(e.which)) {
        keyCodeMap[e.which].style.opacity = 1;
    }
    
}

/*
Called when mouse hovers over keys
Displays key types
*/
function showKeyTypes() {
    for (var i = 0, len = keyTypesW.length; i < len; i++) {
        keyTypesW[i].style.display = 'block';
    }

    for (var i = 0, len = keyTypesB.length; i < len; i++) {
        keyTypesB[i].style.display = 'block';
    }

}

/*
Called when mouse hover leaves keys
Removes key types
*/
function removeKeyTypes() {
    for (var i = 0, len = keyTypesW.length; i < len; i++) {
        keyTypesW[i].style.display = 'none';
    }

    for (var i = 0, len = keyTypesB.length; i < len; i++) {
        keyTypesB[i].style.display = 'none';
    }
}