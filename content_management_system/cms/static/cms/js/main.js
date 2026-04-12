/**
 * Dynamic Content Management System – Main JavaScript
 * Handles AJAX modal loading, accordion, and inline explanation triggers
 */

document.addEventListener('DOMContentLoaded', function () {

    // ═══════════════════════════════════════════
    //  1. AJAX MODAL – Content Items
    // ═══════════════════════════════════════════
    const dynamicModal = document.getElementById('dynamicModal');
    const modalContentWrapper = document.getElementById('modal-content-wrapper');

    if (dynamicModal) {
        dynamicModal.addEventListener('show.bs.modal', function (event) {
            const trigger = event.relatedTarget;
            if (!trigger) return;

            const url = trigger.getAttribute('data-url');
            const isPremium = trigger.getAttribute('data-is-premium');

            // Reset modal to loading state
            modalContentWrapper.innerHTML = `
                <div class="modal-loading">
                    <div class="spinner-border text-primary" role="status"></div>
                    <p>Loading content...</p>
                </div>
            `;

            // Fetch partial HTML via AJAX
            if (url) {
                fetch(url, {
                    headers: { 'X-Requested-With': 'XMLHttpRequest' }
                })
                .then(response => {
                    if (!response.ok) throw new Error('Network error');
                    return response.text();
                })
                .then(html => {
                    modalContentWrapper.innerHTML = html;
                    // Re-bind explanation links inside modal content
                    bindExplanationLinksInRichContent(modalContentWrapper);
                })
                .catch(error => {
                    modalContentWrapper.innerHTML = `
                        <div class="modal-header modal-header-custom">
                            <h5 class="modal-title">Error</h5>
                            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body modal-body-custom">
                            <div class="no-media-placeholder">
                                <i class="bi bi-exclamation-triangle"></i>
                                <p>Failed to load content. Please try again.</p>
                            </div>
                        </div>
                    `;
                    console.error('Modal load error:', error);
                });
            }
        });

        // Clean up media when modal hides (stop audio/video)
        dynamicModal.addEventListener('hidden.bs.modal', function () {
            const audios = modalContentWrapper.querySelectorAll('audio');
            const videos = modalContentWrapper.querySelectorAll('video');
            const iframes = modalContentWrapper.querySelectorAll('iframe');

            audios.forEach(a => { a.pause(); a.currentTime = 0; });
            videos.forEach(v => { v.pause(); v.currentTime = 0; });
            iframes.forEach(f => { f.src = ''; });
        });
    }

    // ═══════════════════════════════════════════
    //  2. AJAX MODAL – Explanation Links
    // ═══════════════════════════════════════════
    const explanationModal = document.getElementById('explanationModal');
    const explanationWrapper = document.getElementById('explanation-content-wrapper');

    if (explanationModal) {
        explanationModal.addEventListener('show.bs.modal', function (event) {
            const trigger = event.relatedTarget;
            if (!trigger) return;

            const url = trigger.getAttribute('data-url');

            explanationWrapper.innerHTML = `
                <div class="modal-loading">
                    <div class="spinner-border text-warning" role="status"></div>
                    <p>Loading explanation...</p>
                </div>
            `;

            if (url) {
                fetch(url, {
                    headers: { 'X-Requested-With': 'XMLHttpRequest' }
                })
                .then(response => {
                    if (!response.ok) throw new Error('Network error');
                    return response.text();
                })
                .then(html => {
                    explanationWrapper.innerHTML = html;
                })
                .catch(error => {
                    explanationWrapper.innerHTML = `
                        <div class="modal-header modal-header-explanation">
                            <h5 class="modal-title">Error</h5>
                            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body modal-body-custom">
                            <div class="no-media-placeholder">
                                <i class="bi bi-exclamation-triangle"></i>
                                <p>Failed to load explanation.</p>
                            </div>
                        </div>
                    `;
                    console.error('Explanation load error:', error);
                });
            }
        });
    }

    // ═══════════════════════════════════════════
    //  3. ACCORDION – Expandable Sections
    // ═══════════════════════════════════════════
    document.querySelectorAll('.accordion-trigger').forEach(function (btn) {
        btn.addEventListener('click', function () {
            const targetId = this.getAttribute('data-target');
            const body = document.getElementById(targetId);
            if (!body) return;

            const isOpen = this.classList.contains('open');

            if (isOpen) {
                this.classList.remove('open');
                this.setAttribute('aria-expanded', 'false');
                body.classList.remove('open');
            } else {
                this.classList.add('open');
                this.setAttribute('aria-expanded', 'true');
                body.classList.add('open');
            }
        });
    });

    // ═══════════════════════════════════════════
    //  4. INLINE EXPLANATION LINKS in Rich Content
    // ═══════════════════════════════════════════
    function bindExplanationLinksInRichContent(container) {
        // Find links with class 'explanation-link' inside rich content
        const explLinks = container.querySelectorAll('.explanation-link, a[data-explanation-id]');
        explLinks.forEach(function (link) {
            link.addEventListener('click', function (e) {
                e.preventDefault();
                const expId = this.getAttribute('data-explanation-id');
                if (expId && explanationModal) {
                    const url = '/explanation/' + expId + '/modal/';
                    explanationWrapper.innerHTML = `
                        <div class="modal-loading">
                            <div class="spinner-border text-warning" role="status"></div>
                            <p>Loading explanation...</p>
                        </div>
                    `;
                    const bsModal = new bootstrap.Modal(explanationModal);
                    fetch(url, {
                        headers: { 'X-Requested-With': 'XMLHttpRequest' }
                    })
                    .then(r => r.text())
                    .then(html => {
                        explanationWrapper.innerHTML = html;
                        bsModal.show();
                    })
                    .catch(() => {
                        explanationWrapper.innerHTML = `
                            <div class="modal-body modal-body-custom">
                                <p>Could not load explanation.</p>
                            </div>`;
                        bsModal.show();
                    });
                }
            });
        });
    }

    // Bind on initial page load
    bindExplanationLinksInRichContent(document);

    // ═══════════════════════════════════════════
    //  5. PREMIUM TOAST NOTIFICATION
    // ═══════════════════════════════════════════
    const premiumToastEl = document.getElementById('premiumToast');
    if (premiumToastEl) {
        const premiumToast = new bootstrap.Toast(premiumToastEl, { delay: 3000 });

        document.querySelectorAll('.media-btn[data-is-premium="true"]').forEach(function (btn) {
            btn.addEventListener('click', function () {
                premiumToast.show();
            });
        });
    }

    // ═══════════════════════════════════════════
    //  6. SMOOTH ENTRANCE ANIMATIONS
    // ═══════════════════════════════════════════
    const observerOptions = { threshold: 0.1, rootMargin: '0px 0px -30px 0px' };
    const fadeObserver = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                fadeObserver.unobserve(entry.target);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.content-card, .sidebar-card').forEach(function (card) {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        fadeObserver.observe(card);
    });

});
