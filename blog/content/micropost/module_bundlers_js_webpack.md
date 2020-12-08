---
title: "Module bundlers"
date: 2020-12-08
description: Micropost on module bundlers in web using webpack
titleWrap: wrap
enableSidebar: false
enableToc: false
---

## Getting started with Webpack

Webpack is a module bundler.  It will make the development job in frontend way
easier, so just use it.  There are alternatives, though webpack is most popular
so I am using it.

Module bundlers automate and optimize much of the effort of working with
frontend.

Add a `webpack.config.js` file to your project:

```js
const path = require('path');

// 1. Install webpack
// npm install --save-dev webpack webpack-cli
//
// 2. Install the modules you want for your project, such as lodash
// npm install --save lodash

module.exports = {
    // 3. Define the entrypoint for your code and output file
    entry: './src/index.js',
    output: {
        filename: 'awesome.js',
        path: path.resolve(__dirname, 'dist'),
    },

    // 4. Add Loaders
    // npm install --save-dev css-loader style-loader sass-loader
    module: {
        rules:[
            {
                test: /\.scss$/,
                use: [
                    'style-loader',
                    'css-loader',
                    'sass-loader',
                ],
            },
        ],
    },

    // 5. Optional add plugin to analyze sizes for optimization
    // npm install --save-dev webpack-bundle-analyzer
    plugins: [
        new BundleAnalyzerPlugin()
    ],

    // 6. Development server
    // npm install --save-dev webpack-dev-server
    devServer: {
        contentBase: path.join(__dirname, 'public')
        port: 9000
    }
};
```

Follow the steps in the file above.

This enables us to use modules in our js files, such as:

```js
import _ from 'lodash'

function component() {
  const element = document.createElement('div');

  // Lodash, now imported by this script
  element.innerHTML = _.join(['Hello', 'webpack'], ' ');

  return element;
}

document.body.appendChild(component());
```

Notice the import!

### Usage

run `npx webpack` or add it to package.json script build stage to use it

use `webpack serve` to run the dev server


## With React

[ref1](https://blog.usejournal.com/creating-a-react-app-from-scratch-f3c693b84658)

React is the most popular SPA framework, so lets add it to our little app

To do this we need to install React

`$ npm install --save-dev react react-dom`

And we need to install babel for transpilation

`$ npm install --save-dev @babel/core @babel/cli @babel/preset-env @babel/preset-react`

Proceed to changing our index.js to a simple react app:

```js
import React from 'react';
import ReactDOM from 'react-dom';

const App = () => (
    <div><h1>Hello world!</h1></div>
)

ReactDOM.render(
    <App/>
    document.getElementById('root')
)
```

In addition we need to add babel as a loader to webpack, in our `webpack.config.js` file:

```js
module.exports = {
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        loader: "babel-loader",
        options: { presets: ["@babel/env"] }
      }
    ]
  }
};
```

And add a `.babelrc` config

```js
{
    "presets": ["@babel/env", "@babel/preset-react"]
}
```
