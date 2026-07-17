const postList = document.querySelector("#post-list");

const formatDate = (date) => new Intl.DateTimeFormat("en", {
    day: "numeric",
    month: "long",
    year: "numeric",
}).format(new Date(date));

const createPostCard = (post) => {
    const article = document.createElement("article");
    article.className = "post-card";

    const content = document.createElement("div");
    content.className = "post-content";

    const date = document.createElement("p");
    date.className = "post-date";
    date.textContent = formatDate(post.date);

    const heading = document.createElement("h3");
    const titleLink = document.createElement("a");
    titleLink.href = post.url;
    titleLink.target = "_blank";
    titleLink.rel = "noopener noreferrer";
    titleLink.textContent = post.title;
    heading.append(titleLink);

    const description = document.createElement("p");
    description.className = "post-description";
    description.textContent = post.description;

    const readLink = document.createElement("a");
    readLink.className = "read-link";
    readLink.href = post.url;
    readLink.target = "_blank";
    readLink.rel = "noopener noreferrer";
    readLink.textContent = "Read post ↗";

    content.append(date, heading, description, readLink);
    article.append(content);

    if (post.image) {
        const image = document.createElement("img");
        image.className = "post-image";
        image.src = post.image;
        image.alt = "";
        image.loading = "lazy";
        article.append(image);
    }

    return article;
};

fetch("posts.json")
    .then((response) => {
        if (!response.ok) throw new Error("Posts could not be loaded");
        return response.json();
    })
    .then((posts) => {
        postList.replaceChildren(...posts.map(createPostCard));
    })
    .catch(() => {
        const message = document.createElement("p");
        message.className = "error-message";
        message.innerHTML = 'Posts are available on <a href="https://substack.com/@stefan0viel/posts">Substack</a>.';
        postList.replaceChildren(message);
    });
