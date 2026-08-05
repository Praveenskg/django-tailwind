/**
 * WanderBook — GSAP animations
 * Requires: gsap.min.js, ScrollTrigger.min.js (loaded in base.html)
 */
(function () {
  "use strict";

  function showAll() {
    document.querySelectorAll(
      "[data-gsap-hero-item], .gsap-reveal, [data-gsap-dash-item]"
    ).forEach(function (el) {
      el.style.opacity = "1";
      el.style.transform = "none";
    });
  }

  if (typeof gsap === "undefined" || typeof ScrollTrigger === "undefined") {
    showAll();
    return;
  }

  var reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reducedMotion) {
    showAll();
    return;
  }

  gsap.registerPlugin(ScrollTrigger);

  var EASE = "power3.out";
  var EASE_SMOOTH = "power2.inOut";

  /* ── Hero timeline (home page) ─────────────────────────── */
  function initHero() {
    var hero = document.querySelector("[data-gsap-hero]");
    if (!hero) return;

    var items = hero.querySelectorAll("[data-gsap-hero-item]");
    var line = hero.querySelector("[data-gsap-hero-line]");
    var heroImg = document.querySelector("[data-gsap-hero-image]");

    if (heroImg) {
      gsap.fromTo(
        heroImg,
        { scale: 1.12 },
        { scale: 1, duration: 20, ease: "power1.out" }
      );
    }

    gsap.set(items, { opacity: 0, y: 48 });

    var tl = gsap.timeline({ defaults: { ease: EASE } });

    tl.to(items, {
      opacity: 1,
      y: 0,
      duration: 0.85,
      stagger: 0.14,
    });

    if (line) {
      gsap.set(line, { scaleX: 0, transformOrigin: "left center" });
      tl.to(
        line,
        { scaleX: 1, duration: 0.9, ease: EASE_SMOOTH },
        "-=0.5"
      );
    }
  }

  /* ── Scroll reveal — single elements ─────────────────────── */
  function initReveal() {
    gsap.utils.toArray(".gsap-reveal").forEach(function (el) {
      gsap.fromTo(
        el,
        { y: 36, opacity: 0 },
        {
          y: 0,
          opacity: 1,
          duration: 0.75,
          ease: EASE,
          scrollTrigger: {
            trigger: el,
            start: "top 88%",
            toggleActions: "play none none none",
          },
        }
      );
    });
  }

  /* ── Scroll reveal — staggered children ──────────────────── */
  function initStagger() {
    gsap.utils.toArray("[data-gsap-stagger]").forEach(function (container) {
      var children = container.children;
      if (!children.length) return;

      gsap.fromTo(
        children,
        { y: 44, opacity: 0 },
        {
          y: 0,
          opacity: 1,
          duration: 0.65,
          stagger: 0.1,
          ease: EASE,
          scrollTrigger: {
            trigger: container,
            start: "top 85%",
            toggleActions: "play none none none",
          },
        }
      );
    });
  }

  /* ── Dashboard entrance ──────────────────────────────────── */
  function initDashboard() {
    var dash = document.querySelector("[data-gsap-dashboard]");
    if (!dash) return;

    var blocks = dash.querySelectorAll("[data-gsap-dash-item]");
    gsap.fromTo(
      blocks,
      { y: 32, opacity: 0 },
      {
        y: 0,
        opacity: 1,
        duration: 0.7,
        stagger: 0.1,
        ease: EASE,
        delay: 0.08,
      }
    );
  }

  /* ── Page heading fade ───────────────────────────────────── */
  function initPageHeading() {
    var heading = document.querySelector("[data-gsap-page-heading]");
    if (!heading) return;

    gsap.fromTo(
      heading,
      { y: 24, opacity: 0 },
      { y: 0, opacity: 1, duration: 0.65, ease: EASE, delay: 0.05 }
    );
  }

  /* ── Card hover lift (subtle, desktop only) ──────────────── */
  function initCardHover() {
    if (window.matchMedia("(max-width: 768px)").matches) return;

    document.querySelectorAll("[data-gsap-hover]").forEach(function (card) {
      card.addEventListener("mouseenter", function () {
        gsap.to(card, { y: -6, duration: 0.35, ease: "power2.out" });
      });
      card.addEventListener("mouseleave", function () {
        gsap.to(card, { y: 0, duration: 0.4, ease: "power2.out" });
      });
    });
  }

  /* ── Run all ─────────────────────────────────────────────── */
  function init() {
    try {
      initHero();
      initDashboard();
      initPageHeading();
      initReveal();
      initStagger();
      initCardHover();
    } catch (err) {
      console.error("GSAP init failed:", err);
      showAll();
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
