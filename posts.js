const postList = document.querySelector("#post-list");

const formatDate = (date) => new Intl.DateTimeFormat("en", {
    day: "numeric",
    month: "long",
    year: "numeric",
}).format(new Date(date));

const createPostCard = (post) => {
    const article = document.createElement("article");
    article.className = "post-card";

    const date = document.createElement("time");
    date.className = "post-date";
    date.dateTime = post.date;
    date.textContent = formatDate(post.date);

    const heading = document.createElement("h3");
    const titleLink = document.createElement("a");
    titleLink.href = post.url;
    titleLink.target = "_blank";
    titleLink.rel = "noopener noreferrer";
    titleLink.textContent = post.title;
    heading.append(titleLink);

    article.append(heading, date);

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
