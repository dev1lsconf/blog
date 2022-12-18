/** @jsx h */

import blog, { ga, redirects, h } from "blog";

blog({
  title: "Dev1ls>Blog",
  description: "OpenBSD and Nixos User.. Learning.",
  header: <header>OpenBSD</header>,
  section: <section>My Logs:</section>,
  footer: <footer>contact: dev1ls@sdf.org</footer>,
  avatar: "https://deno-avatar.deno.dev/avatar/blog.svg",
  avatarClass: "rounded-full",
  author: "An author",

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
