/** @jsx h */

import blog, { ga, redirects, h } from "blog";

blog({
  title: "Dev1ls>Blog",
  description: "Unix Lover / learning VM, Networking, python and Backend Services..",
  // header: <header>Dev1ls' Blog</header>,
  // section: <section>My Logs:</section>,
 // `` footer: <footer>contact: dev1ls@sdf.org</footer>,
  avatar: "beastie.png",
  avatarClass: "rounded-full",
  author: "Dev1ls",
  dateStyle: "long",
  links: [
    { title: "Email", url: "mailto:dev1ls@texto-plano.xyz" },
    { title: "GitHub", url: "https://github.com/dev1lsconf" },
    { title: "Twitter", url: "https://twitter.com/dev1lsconf" },
    { title: "Mastodon", url: "https://mastodon.sdf.org/@dev1ls"},

  ],
  // middlewares: [

    // If you want to set up Google Analytics, paste your GA key here.
    // ga("UA-XXXXXXXX-X"),

    // If you want to provide some redirections, you can specify them here,
    // pathname specified in a key will redirect to pathname in the value.
    // redirects({
    //  "/hello_world.html": "/hello_world",
    // }),

  // ]

});
