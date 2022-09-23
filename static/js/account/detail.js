let profile = document.querySelector('#profile')
let scale = 1
let prevScrollY = 0
let windowHeight10 = window.innerHeight * (20 / 100)

window.onscroll = () => {
	scale = (windowHeight10 - window.scrollY) / windowHeight10
	if (scale < .6) {
		scale = .6
	}
	if (scale > 1) {
		scale = 1
	}
	profile.style.transform = `scale(${scale})`
	prevScrollY = window.scrollY
	console.log(windowHeight10)
}

document.querySelector("#back").onclick = () => {
	history.back()
}

let tab = document.querySelectorAll("[name='tab']")
tab.forEach((e, index) => {
	e.onclick = () => {
		if (e.checked) {
			document.querySelector("#tabs").style.transform = `translateX(-${index * 100}%)`
		}
	}
})

let cover = document.getElementById("cover")
let nav = document.getElementById("nav")
let observer = new IntersectionObserver((entries, observer) => {
	for (const entry of entries) {
		if (entry.target == cover && entry.isIntersecting) {
			nav.style.background = 'rgb(96 165 250 / var(--tw-bg-opacity))'
		} else {
			nav.style.background = 'black'
		}
	}
}, {
	root: null,
	threshold: 1,
	rootMargin: "56px 0px 0px 0px"
})
observer.observe(cover)
