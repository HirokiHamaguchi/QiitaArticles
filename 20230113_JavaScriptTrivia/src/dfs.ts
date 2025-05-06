interface XY {
  x: number;
  y: number;
}

function dfs(adj: number[][], ans: XY[], v: number, xy: XY) {
  ans[v] = xy;

  // 行きがけ時の処理
  xy.x += 1;

  for (const nv of adj[v]) dfs(adj, ans, nv, xy);

  // 帰りがけ時の処理
  xy.x -= 1;
  if (adj[v].length === 0) xy.y += 1;
}

function main() {
  const adj = [[1, 5, 6], [2], [3, 4], [], [], [], [7, 8], [], []];
  const ans = new Array(adj.length);

  let xy = { x: 0, y: 0 };

  dfs(adj, ans, 0, xy);

  // 答えの確認
  for (const xy of ans) {
    console.log(xy);
  }

  return 0;
}

main();
