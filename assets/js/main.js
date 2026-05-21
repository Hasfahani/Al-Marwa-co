/*
	Forty by HTML5 UP
	html5up.net | @ajlkn
	Free for personal and commercial use under the CCA 3.0 license (html5up.net/license)
*/

(function() {
	var windowEl = window,
		bodyEl = document.body,
		wrapperEl = document.getElementById('wrapper'),
		headerEl = document.getElementById('header'),
		bannerEl = document.getElementById('banner');

	function on(target, event, handler, options) {
		if (target)
			target.addEventListener(event, handler, options || false);
	}

	function off(target, event, handler) {
		if (target)
			target.removeEventListener(event, handler);
	}

	function triggerScroll() {
		windowEl.dispatchEvent(new Event('scroll'));
	}

	function getDocumentTop(element) {
		return element.getBoundingClientRect().top + (windowEl.pageYOffset || document.documentElement.scrollTop || 0);
	}

	function smoothScrollTo(top, duration) {
		var start = windowEl.pageYOffset || document.documentElement.scrollTop || 0,
			change = top - start,
			startTime = null;

		function ease(t) {
			return t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
		}

		function animate(currentTime) {
			if (startTime === null)
				startTime = currentTime;

			var progress = Math.min((currentTime - startTime) / duration, 1);
			windowEl.scrollTo(0, start + change * ease(progress));

			if (progress < 1)
				windowEl.requestAnimationFrame(animate);
		}

		windowEl.requestAnimationFrame(animate);
	}

	// Breakpoints.
	breakpoints({
		xlarge:    ['1281px',   '1680px'   ],
		large:     ['981px',    '1280px'   ],
		medium:    ['737px',    '980px'    ],
		small:     ['481px',    '736px'    ],
		xsmall:    ['361px',    '480px'    ],
		xxsmall:   [null,       '360px'    ]
	});

	function parallax(element, intensity) {
		var disabled = browser.name == 'ie' || browser.name == 'edge' || browser.mobile;

		if (!element || disabled || intensity === 0)
			return;

		if (!intensity)
			intensity = 0.25;

		function onScroll() {
			var pos = parseInt(windowEl.pageYOffset || document.documentElement.scrollTop || 0) - parseInt(getDocumentTop(element));
			element.style.backgroundPosition = 'center ' + (pos * (-1 * intensity)) + 'px';
		}

		function enable() {
			element.style.backgroundPosition = 'center 100%, center 100%, center 0px';
			off(windowEl, 'scroll', onScroll);
			on(windowEl, 'scroll', onScroll);
			onScroll();
		}

		function disable() {
			element.style.backgroundPosition = '';
			off(windowEl, 'scroll', onScroll);
		}

		breakpoints.on('<=medium', disable);
		breakpoints.on('>medium', enable);
		on(windowEl, 'load', onScroll);
		on(windowEl, 'resize', onScroll);
	}

	// Play initial animations on page load.
	on(windowEl, 'load', function() {
		window.setTimeout(function() {
			bodyEl.classList.remove('is-preload');
		}, 100);
	});

	// Clear transitioning state on unload/hide.
	on(windowEl, 'unload', clearTransitioning);
	on(windowEl, 'pagehide', clearTransitioning);

	function clearTransitioning() {
		window.setTimeout(function() {
			document.querySelectorAll('.is-transitioning').forEach(function(element) {
				element.classList.remove('is-transitioning');
			});
		}, 250);
	}

	// IE-only tweaks.
	if (browser.name == 'ie' || browser.name == 'edge')
		bodyEl.classList.add('is-ie');

	// Scrolly.
	document.querySelectorAll('.scrolly[href^="#"]').forEach(function(link) {
		on(link, 'click', function(event) {
			var target = document.querySelector(link.getAttribute('href'));

			if (!target)
				return;

			event.preventDefault();
			smoothScrollTo(getDocumentTop(target) - ((headerEl ? headerEl.offsetHeight : 0) - 2), 500);
		});
	});

	// Tiles.
	document.querySelectorAll('.tiles > article').forEach(function(tile) {
		var image = tile.querySelector('.image'),
			img = image ? image.querySelector('img') : null,
			link = tile.querySelector('.link');

		if (img) {
			tile.style.backgroundImage = 'url(' + img.getAttribute('src') + ')';

			if (img.dataset.position)
				image.style.backgroundPosition = img.dataset.position;

			if (image)
				image.style.display = 'none';
		}

		if (link) {
			var overlayLink = link.cloneNode(true);

			overlayLink.textContent = '';
			overlayLink.classList.add('primary');
			tile.appendChild(overlayLink);

			[link, overlayLink].forEach(function(activeLink) {
				on(activeLink, 'click', function(event) {
					var href = activeLink.getAttribute('href');

					event.stopPropagation();
					event.preventDefault();

					if (activeLink.getAttribute('target') == '_blank') {
						window.open(href);
						return;
					}

					tile.classList.add('is-transitioning');
					if (wrapperEl)
						wrapperEl.classList.add('is-transitioning');

					window.setTimeout(function() {
						location.href = href;
					}, 500);
				});
			});
		}
	});

	// Header.
	if (bannerEl && headerEl && headerEl.classList.contains('alt')) {
		function updateHeader() {
			var bottom = getDocumentTop(bannerEl) + bannerEl.offsetHeight,
				scrollTop = windowEl.pageYOffset || document.documentElement.scrollTop || 0,
				threshold = (headerEl.offsetHeight || 0) + 10;

			if (scrollTop + threshold < bottom) {
				headerEl.classList.add('alt');
				headerEl.classList.remove('reveal');
			} else {
				headerEl.classList.remove('alt');
				headerEl.classList.add('reveal');
			}
		}

		on(windowEl, 'scroll', updateHeader);
		on(windowEl, 'resize', updateHeader);
		on(windowEl, 'load', function() {
			window.setTimeout(updateHeader, 100);
		});
	}

	// Banner.
	if (bannerEl) {
		var bannerImage = bannerEl.querySelector('.image'),
			bannerImg = bannerImage ? bannerImage.querySelector('img') : null;

		parallax(bannerEl, 0);

		if (bannerImg) {
			bannerEl.style.backgroundImage = 'url(' + bannerImg.getAttribute('src') + ')';
			bannerImage.style.display = 'none';
		}
	}

	// Menu.
	var menuEl = document.getElementById('menu'),
		menuInnerEl,
		menuLocked = false;

	if (menuEl) {
		menuInnerEl = document.createElement('div');
		menuInnerEl.className = 'inner';

		while (menuEl.firstChild)
			menuInnerEl.appendChild(menuEl.firstChild);

		menuEl.appendChild(menuInnerEl);
		bodyEl.appendChild(menuEl);

		function lockMenu() {
			if (menuLocked)
				return false;

			menuLocked = true;
			window.setTimeout(function() {
				menuLocked = false;
			}, 350);

			return true;
		}

		function showMenu() {
			if (lockMenu())
				bodyEl.classList.add('is-menu-visible');
		}

		function hideMenu() {
			if (lockMenu())
				bodyEl.classList.remove('is-menu-visible');
		}

		function toggleMenu() {
			if (lockMenu())
				bodyEl.classList.toggle('is-menu-visible');
		}

		on(menuInnerEl, 'click', function(event) {
			event.stopPropagation();
		});

		menuInnerEl.querySelectorAll('a').forEach(function(link) {
			on(link, 'click', function(event) {
				var href = link.getAttribute('href');

				event.preventDefault();
				event.stopPropagation();
				hideMenu();

				window.setTimeout(function() {
					window.location.href = href;
				}, 250);
			});
		});

		on(menuEl, 'click', function(event) {
			event.stopPropagation();
			event.preventDefault();
			bodyEl.classList.remove('is-menu-visible');
		});

		var closeLink = document.createElement('a');
		closeLink.className = 'close';
		closeLink.href = '#menu';
		closeLink.textContent = 'Close';
		menuEl.appendChild(closeLink);

		document.querySelectorAll('a[href="#menu"]').forEach(function(link) {
			on(link, 'click', function(event) {
				event.stopPropagation();
				event.preventDefault();
				toggleMenu();
			});
		});

		on(bodyEl, 'click', hideMenu);
		on(bodyEl, 'keydown', function(event) {
			if (event.keyCode == 27)
				hideMenu();
		});
	}

	// Scroll-to-top button.
	var scrollBtn = document.createElement('button');
	scrollBtn.className = 'scroll-top-btn';
	scrollBtn.setAttribute('aria-label', 'Scroll to top');
	scrollBtn.innerHTML = '<span class="icon solid fa-chevron-up" aria-hidden="true"></span>';
	bodyEl.appendChild(scrollBtn);

	on(windowEl, 'scroll', function() {
		if ((windowEl.pageYOffset || document.documentElement.scrollTop || 0) > 400)
			scrollBtn.classList.add('visible');
		else
			scrollBtn.classList.remove('visible');
	});

	on(scrollBtn, 'click', function() {
		smoothScrollTo(0, 380);
	});

	triggerScroll();
})();
