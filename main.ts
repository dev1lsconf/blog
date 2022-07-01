import blog, { ga, redirects } from "https://deno.land/x/blog@0.3.3/blog.tsx";
import { white } from "https://deno.land/std/fmt/colors.ts"

blog({
  title: "Dev1ls > Blog",
  description: "Blog sobre Linux y desarrollo de aplicaciones.",
  cover: "https://media.giphy.com/media/3o7TKolyPUm9BhVwiY/giphy.gif",
  coverStyle: "rounded",
  author: "Dev1ls",
  background: "#f9f9f9",
  links: [
    { title: "Email", url: "mailto:dev1lsconf@gmail.com" },
    { title: "GitHub", url: "https://github.com/dev1lsconf" },
    { title: "Twitter", url: "https://twitter.com/dev1lsconf" },
  ],
  lang: "es",
  timezone: "en-US",

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
