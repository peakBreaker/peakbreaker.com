---
categories: Blender
description: Overview, models & texturing
featured_image: covers/blender.png
author: Anders
title: CGI for Engineers Pt. 1
finished: true
date: "2018-04-08"
layout: post
tags: ['blender', '3d', 'modelling']
---
## Blender is great
Blender is an open source 3D computer graphics software for creating pretty much whatever you can imagine in 3D.

It is a pretty awesome piece of software, entirely free as in beer and speech, with a great amount of features for creating professional level content.  In the hands of a trained person the results can be quite astonishing. Just take a look at this short film made by the blender foundation itself:

<div class="responsive_iframe">
  <iframe width="560" height="315" src="https://www.youtube.com/embed/aqz-KE-bpKQ" frameborder="0" allowfullscreen></iframe>
</div>

### Thats cool, but..
Youre not going to be a professional 3D artist. Or if you are then this post is not meant for you.  You're into engineering and making products and stuff, so why would you ever need CGI?

**Why learn blender / CGI as an engineer?** Engineers will find themselves making models using CAD software from time to time. Or design systems which requires a lot of learning for other people to comprehend. Your goal will always be to work with other people and sell forward your product, and therefore you must be able to show off your work. Knowing blender for 3d graphics together with inkscape for vectorgraphics and gimp for photoshop can give you a very powerful stack for displaying your work. Don't get me wrong though - blender is not CAD software.

In addition Blender is a fun and versatile software, and as an engineer your job is to be the king of tools. The job description of an engineer is someone who can create awesome stuff, and gripping the basics of CGI and blender will help pursuing this goal. Convinced? Great!

### Interesting, can we get our hands dirty now?

Yes! Time for the fun part - Lets look at some super simple basics of blender!

To create a textured model there are basically 3 things we need to do:
- Create the mesh (modelling)
- Mapping our mesh and applying textures
- Adding our materials


Allright, lets try to make this low poly tombstone to just get a grip of the basics:

![Blender render](/assets/img/blender/blender1-1.png)

[I just found it as a simple model to make to understand the basic principles]

#### Model:
1. We can use the default cube when opening a new scene, or create a new cube by pressing **Shift-A** -> mesh -> cube
2. To edit the cube object we enter edit mode by selecting the cube and pressing **Tab**
3. At the lower part of the window you see this (see below) which will let you select vertex/edge/face ![Select vertex/edge/face](/assets/img/blender/blender1-2.png)
4. To make the model we select different vertecies/edges and faces and use **G** to move them about and **S** to scale the selections, and extrude new elements with **E** - You just have to try about things till you have what looks good.
5. Finally you should have something that looks like this
![Final mesh](/assets/img/blender/blender1-3.png)

#### Mapping, materials and texturing:

1. First we gotta UV map our model. If you dont know what this is, google it and read abit on the wiki page for the subject. The first part of this in blender is to mark seams. Select edges (in edit mode), hit **CTRL-E** and mark seam. Seams are where our unwrapper cannot stitch our UV map.
2. After getting our seams correct we can unwrap our model.  Select all vertecies/edges/faces on our model with **A** and hit **U** and -> Unwrap
3. Bring up a pane with with UV/Image editor, add an image
![Adding a new texture image](/assets/img/blender/blender1-4.png)
4. One would typically check and alter the UV map with a checkerpattern now, but we will skip this step in this tut
5. We will now add our material. Make sure you are using cycles render as the rendering engine (set this in upper right corner), go to the materials tab (see below), and create a new material. On the material, make sure you are using nodes.
![Materials tab](/assets/img/blender/blender1-5.png)
6. Enter node editor, add a Image Texture node with **SHIFT-A** -> Texture -> Image Texture and put the output to a diffuse shader node which has its output to the Material output.
![Node Editor](/assets/img/blender/blender1-6.png)
7. We can now enter texture mode and start texturing our model! ![Texture painting](/assets/img/blender/blender1-7.png)

Now make the model like you want it

Hope you enjoyed this tut, I know I did. See you later! :)
