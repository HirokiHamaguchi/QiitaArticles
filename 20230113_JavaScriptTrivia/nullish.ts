function veryVeryLongFuntionName(x) {
  return 0;
}

function f(x: number): number | undefined {
  if (x != 0) {
    return (x - 1) / x;
  } else {
    return undefined;
  }
}

console.log(f(0.5)); // -1
console.log(f(0)); // undefined
console.log(f(0) || 123); // 123
console.log(f(1)); // 0
console.log(f(1) || 123); // 123

console.log(veryVeryLongFuntionName(1) !== null ? veryVeryLongFuntionName(1) : 123);

// 可読性が下がりますし、なによりこのままだと関数呼び出しが2回発生してしまいます。一時変数を用意しても良いのですが、そうするとわざわざconstでなくletで宣言する必要があったり、コードを書くのが面倒だったりします。

// そんな悩みを解決してくれるのが`??`演算子です。

console.log(f(0) ?? 123); // 123
console.log(f(1) ?? 123); // 0
