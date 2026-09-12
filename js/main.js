// Renders the latest Substack posts from data/posts.json, which is refreshed
// on a schedule by .github/workflows/sync-posts.yml.

(function () {
    var grid = document.getElementById('essays-grid');
    if (!grid) return;

    function formatDate(iso) {
        if (!iso) return '';
        var d = new Date(iso + 'T12:00:00Z');
        return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
    }

    function el(tag, className, text) {
        var node = document.createElement(tag);
        if (className) node.className = className;
        if (text) node.textContent = text;
        return node;
    }

    function card(post, featured) {
        var a = el('a', featured ? 'essay essay-featured' : 'essay');
        a.href = post.url;
        a.target = '_blank';
        a.rel = 'noopener';

        if (post.image) {
            var wrap = el('div', 'essay-image');
            var img = el('img');
            img.src = post.image;
            img.alt = '';
            img.loading = 'lazy';
            wrap.appendChild(img);
            a.appendChild(wrap);
        }

        var body = el('div', 'essay-body');
        body.appendChild(el('h3', 'essay-title', post.title));
        if (post.subtitle) body.appendChild(el('p', 'essay-subtitle', post.subtitle));
        body.appendChild(el('p', 'essay-date', formatDate(post.date)));
        a.appendChild(body);
        return a;
    }

    function fallback() {
        var p = el('p', 'essays-fallback');
        p.appendChild(document.createTextNode('Read the essays at '));
        var link = el('a', null, 'travisknudsen.substack.com');
        link.href = 'https://travisknudsen.substack.com';
        p.appendChild(link);
        p.appendChild(document.createTextNode('.'));
        grid.appendChild(p);
    }

    fetch('data/posts.json', { cache: 'no-cache' })
        .then(function (r) { return r.ok ? r.json() : Promise.reject(r.status); })
        .then(function (data) {
            var posts = (data && data.posts) || [];
            if (!posts.length) return fallback();
            grid.appendChild(card(posts[0], true));
            var rest = el('div', 'essay-list');
            posts.slice(1, 5).forEach(function (p) { rest.appendChild(card(p, false)); });
            grid.appendChild(rest);
        })
        .catch(fallback);
})();
