// The Theory of Conscious Creation - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
      // Mobile Navigation Toggle
                              const navToggle = document.querySelector('.nav-toggle');
      const navLinks = document.querySelector('.nav-links');

                              if (navToggle && navLinks) {
                                        navToggle.addEventListener('click', function() {
                                                      navLinks.classList.toggle('active');
                                                      navToggle.classList.toggle('active');
                                        });

          // Close mobile menu when clicking a link
          navLinks.querySelectorAll('a').forEach(link => {
                        link.addEventListener('click', () => {
                                          navLinks.classList.remove('active');
                                          navToggle.classList.remove('active');
                        });
          });
                              }

                              // Smooth scroll for anchor links
                              document.querySelectorAll('a[href^="#"]').forEach(anchor => {
                                        anchor.addEventListener('click', function(e) {
                                                      e.preventDefault();
                                                      const target = document.querySelector(this.getAttribute('href'));
                                                      if (target) {
                                                                        const navHeight = document.querySelector('.nav').offsetHeight;
                                                                        const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - navHeight;
                                                                        window.scrollTo({
                                                                                              top: targetPosition,
                                                                                              behavior: 'smooth'
                                                                        });
                                                      }
                                        });
                              });

                              // Navbar background on scroll
                              const nav = document.querySelector('.nav');
      let lastScroll = 0;

                              window.addEventListener('scroll', function() {
                                        const currentScroll = window.pageYOffset;
                                        if (currentScroll > 100) {
                                                      nav.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.1)';
                                        } else {
                                                      nav.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.05)';
                                        }
                                        lastScroll = currentScroll;
                              });

                              // Intersection Observer for fade-in animations
                              const observerOptions = {
                                        root: null,
                                        rootMargin: '0px',
                                        threshold: 0.1
                              };

                              const observer = new IntersectionObserver((entries) => {
                                        entries.forEach(entry => {
                                                      if (entry.isIntersecting) {
                                                                        entry.target.classList.add('visible');
                                                                        observer.unobserve(entry.target);
                                                      }
                                        });
                              }, observerOptions);

                              // Observe all sections
                              document.querySelectorAll('.section').forEach(section => {
                                        observer.observe(section);
                              });

                              // Newsletter form handling
                              const newsletterForm = document.querySelector('.newsletter-form');
      if (newsletterForm) {
                newsletterForm.addEventListener('submit', function(e) {
                              // Form will submit to Buttondown
                                                            // Add any additional validation here if needed
                                                            const email = this.querySelector('input[type="email"]').value;
                              if (!email || !email.includes('@')) {
                                                e.preventDefault();
                                                alert('Please enter a valid email address.');
                              }
                });
      }

                              console.log('The Theory of Conscious Creation - Site Loaded');
});
