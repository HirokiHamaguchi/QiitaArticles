/*
 * ATTENTION: The "eval" devtool has been used (maybe by default in mode: "development").
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
/******/ (() => { // webpackBootstrap
/******/ 	"use strict";
/******/ 	var __webpack_modules__ = ({

/***/ "./src/index.ts":
/*!**********************!*\
  !*** ./src/index.ts ***!
  \**********************/
/***/ (() => {

eval("\r\nvar BUTTON = document.getElementById(\"trigger\");\r\nvar LOADING = document.getElementById(\"loading\");\r\nBUTTON.addEventListener(\"click\", function () {\r\n    LOADING.hidden = false; // グルグルを表示させる\r\n    // 何らかの非常に重い処理\r\n    for (var i = 0; i <= 100000000; i++) {\r\n        if (i % 10000000 == 0)\r\n            console.log(\"progress: \".concat(i / 1000000, \"%\"));\r\n        Math.random();\r\n    }\r\n    console.log(\"done.\");\r\n    LOADING.hidden = true; // グルグルを非表示にさせる\r\n});\r\n//   setTimeout(() => {}, 100);\r\n\n\n//# sourceURL=webpack://my-webpack-project/./src/index.ts?");

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	// This entry module can't be inlined because the eval devtool is used.
/******/ 	var __webpack_exports__ = {};
/******/ 	__webpack_modules__["./src/index.ts"]();
/******/ 	
/******/ })()
;