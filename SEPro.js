import { DotLottie } from "https://esm.sh/@lottiefiles/dotlottie-web";

const SPARKLE_URL =
	"https://lottie.host/aa8461b8-0395-40aa-9916-3aa8737d127d/wgZlYJ42zU.lottie";

const word = document.querySelector("#word");
const sparkElement = document.querySelector(".spark");

const canvas = document.createElement("canvas");
canvas.width = 240;
canvas.height = 240;
canvas.className = "spark-canvas";
sparkElement.appendChild(canvas);

const player = new DotLottie({
	canvas: canvas,
	loop: true,
	autoplay: false,
	src: SPARKLE_URL,
	renderConfig: {
		clearCanvas: true,
		backgroundAlpha: 0,
		devicePixelRatio: Math.min(2, window.devicePixelRatio || 1)
	}
});

player.setSpeed(1);

const prefersReduced = window.matchMedia("(prefers-reduced-motion: reduce)")
	.matches;
if (prefersReduced) {
	setSparkles(false);
} else {
	setSparkles(false);
}

word.addEventListener("mouseenter", () => {
	setSparkles(true);
});

word.addEventListener("mouseleave", () => {
	setSparkles(false);
});

function setSparkles(isOn) {
	document.documentElement.toggleAttribute("data-sparkles", isOn ? "on" : "off");
	if (isOn) {
		player.play();
	} else {
		player.pause();
	}
}

setSparkles(false);

