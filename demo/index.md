---
title: The Monospace Web (Python Edition)
subtitle: A minimalist design exploration, rebuilt with duct tape and Python
author: Christopher C. Smith
author-url: "https://github.com/chriscarrollsmith"
lang: en
toc-title: Contents
---

## Introduction

This is a Python-powered replication of [The Monospace Web](https://github.com/owickstrom/the-monospace-web) by Oskar Wickström. 
Where the original uses Nix, Pandoc, and Make (a sophisticated, principled approach), this version uses Python, Jinja2, and duct tape (an "it works on my machine" approach).

Monospace fonts are dear to many of us. 
Some find them more readable, consistent, and beautiful, than their proportional alternatives.
Maybe we're just brainwashed from spending years in terminals?
Or are we hopelessly nostalgic?
I'm not sure.
But I like them, and that's why I started experimenting with all-monospace Web.

On this page, I use a monospace grid to align text and draw diagrams.
It's generated from a simple Markdown document (using Python-Markdown instead of Pandoc), and the CSS and a tiny bit of Javascript renders it on the grid.
The page is responsive, shrinking in character-sized steps.
Standard elements should _just work_, at least that's the goal.
It's semantic HTML, rendered as if we were back in the 70s.

All right, but is this even a good idea?
It's a technical and creative challenge and I like the aesthetic.
The original project is much more sophisticated - this is just me having fun rebuilding it with my favorite tools.
If you'd like to use it, feel free to fork or copy the bits you need, respecting the license.
I might update it over time with improvements and support for more standard elements.

## The Basics

This document uses a few extra classes here and there, but mostly it's just markup.
This, for instance, is a regular paragraph.

Look at this horizontal break:

<hr>

Lovely. We can hide stuff in the `<details`> element:

<details>
<summary>A short summary of the contents</summary>
<p>Hidden gems.</p>
</details>

## Lists

This is a plain old bulleted list:

* Banana
* Paper boat
* Cucumber
* Rocket

Ordered lists look pretty much as you'd expect:

1. Goals
1. Motivations
    1. Intrinsic
    1. Extrinsic
1. Second-order effects

It's nice to visualize trees.
This is a regular unordered list with a `tree` class:

<ul class="tree">
<li>
<p style="margin: 0;"><strong>/dev/nvme0n1p2</strong></p>
<ul>
<li>usr
<ul>
<li>local<br /></li>
<li>share<br /></li>
<li>libexec<br /></li>
<li>include<br /></li>
<li>sbin<br /></li>
<li>src<br /></li>
<li>lib64<br /></li>
<li>lib<br /></li>
<li>bin<br /></li>
<li>games
<ul>
<li>solitaire</li>
<li>snake</li>
<li>tic-tac-toe</li>
</ul></li>
<li>media<br /></li>
</ul></li>
<li>media<br /></li>
<li>run<br /></li>
<li>tmp</li>
</ul>
</li>
</ul>

## Tables

We can use regular tables that automatically adjust to the monospace grid.
They're responsive. 

<table>
<thead>
  <tr>
    <th class="width-min">Name</th>
    <th class="width-auto">Dimensions</th>
    <th class="width-min">Position</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>Boboli Obelisk</td>
    <td>1.41m &times; 1.41m &times; 4.87m</td>
    <td>43°45'50.78"N 11°15'3.34"E</td>
  </tr>
  <tr>
    <td>Pyramid of Khafre</td>
    <td>215.25m &times; 215.25m &times; 136.4m</td>
    <td>29°58'34"N 31°07'51"E</td>
  </tr>
</tbody>
</table>

Note that only one column is allowed to grow.

## Forms

Here are some buttons:

<nav>
    <button>Reset</button>
    <button>Save</button>
</nav>

And inputs:

<form class="grid">
<label>First name <input type="text" placeholder="Placeholder..." /></label>
<label>Last name <input type="text" placeholder="Text goes here..." /></label>
<label>Age <input type="text" value="30" /></label>
</form>

And radio buttons:

<form class="grid">
<label><input name="radio" type="radio" /> Option #1</label>
<label><input name="radio" type="radio" /> Option #2</label>
<label><input name="radio" type="radio" /> Option #3</label>
</form>

## Grids

Add the `grid` class to a container to divide up the horizontal space evenly for the cells.
Note that it maintains the monospace, so the total width might not be 100%.
Here are six grids with increasing cell count:

<div class="grid"><input readonly value="1" /></div>
<div class="grid"><input readonly value="1" /><input readonly value="2" /></div>
<div class="grid"><input readonly value="1" /><input readonly value="2" /><input readonly value="3" /></div>
<div class="grid"><input readonly value="1" /><input readonly value="2" /><input readonly value="3" /><input readonly value="4" /></div>
<div class="grid"><input readonly value="1" /><input readonly value="2" /><input readonly value="3" /><input readonly value="4" /><input readonly value="5" /></div>
<div class="grid"><input readonly value="1" /><input readonly value="2" /><input readonly value="3" /><input readonly value="4" /><input readonly value="5" /><input readonly value="6" /></div>

If we want one cell to fill the remainder, we set `flex-grow: 1;` for that particular cell.

<div class="grid"><input readonly value="1" /><input readonly value="2" /><input readonly value="3!" style="flex-grow: 1;" /><input readonly value="4" /><input readonly value="5" /><input readonly value="6" /></div>

## ASCII Drawings

We can draw in `<pre>` tags using [box-drawing characters](https://en.wikipedia.org/wiki/Box-drawing_characters):

```
╭─────────────────╮
│ MONOSPACE ROCKS │
╰─────────────────╯
```

To have it stand out a bit more, we can wrap it in a `<figure>` tag, and why not also add a `<figcaption>`.

<figure>
<pre>
┌───────┐ ┌───────┐ ┌───────┐
│Actor 1│ │Actor 2│ │Actor 3│
└───┬───┘ └───┬───┘ └───┬───┘
    │         │         │    
    │         │  msg 1  │    
    │         │────────►│    
    │         │         │    
    │  msg 2  │         │    
    │────────►│         │    
┌───┴───┐ ┌───┴───┐ ┌───┴───┐
│Actor 1│ │Actor 2│ │Actor 3│
└───────┘ └───────┘ └───────┘</pre>
<figcaption>Example: Message passing.</figcaption>
</figure>

Let's go wild and draw a chart!

<figure><pre>
                      Things I Have
                                              
    │                                     ████ Usable
15  │
    │                                     ░░░░ Broken
    │
12  │             ░            
    │             ░            
    │   ░         ░              
 9  │   ░         ░              
    │   ░         ░              
    │   ░         ░                    ░
 6  │   █         ░         ░          ░
    │   █         ░         ░          ░
    │   █         ░         █          ░
 3  │   █         █         █          ░
    │   █         █         █          ░
    │   █         █         █          ░
 0  └───▀─────────▀─────────▀──────────▀─────────────
      Socks     Jeans     Shirts   USB Drives
</pre></figure>

## Media

Media objects are supported, like images and video:

![A room in an old French castle (2024)](castle.jpg)

![[The Center of the Web (1914), Wikimedia](https://en.wikisource.org/wiki/Page:The_Center_of_the_Web_(1914).webm/11)](https://upload.wikimedia.org/wikipedia/commons/e/e0/The_Center_of_the_Web_%281914%29.webm)

They extend to the width of the page, and add appropriate padding in the bottom to maintain the monospace grid.

## Discussion

That's it for now.
I've very much enjoyed making this, pushing my Python and Jinja2 chops and having a lot of fun with the design.
If you like it or even decide to use it, please [let me know](https://github.com/chriscarrollsmith/monospace-web-python).

The full source code is here: [github.com/chriscarrollsmith/monospace-web-python](https://github.com/chriscarrollsmith/monospace-web-python)

A massive shout-out to [Oskar Wickström](https://github.com/owickstrom) for the original design and inspiration, and to [U.S. Graphics Company](https://x.com/usgraphics) for the monospace aesthetic that inspired us both.

This site is automatically deployed using GitHub Actions, because apparently we can't just use `make` like normal people.
