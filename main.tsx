/** @jsx h */

import blog, { ga, redirects, h } from "blog";

blog({
  title: "Dev1ls",
  description: "Blog about my experiences with OpenBSD and Nixos",
  //header: <header>OpenBSD</header>,
  //section: <section>My Logs:</section>,
  //footer: <footer>contact: dev1ls@sdf.org</footer>,
  avatar: "beastie.png",
  avatarClass: "rounded-full",
  author: "Dev1ls",

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
