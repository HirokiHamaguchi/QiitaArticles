import "./main";

// allowUnreachableCode
function fn(n: number) {
  if (n > 5) {
    return true;
  } else {
    return false;
  }
  return true;
}

// allowUnusedLabels
function verifyAge(age: number) {
  // 'return'の記述が抜けている
  if (age > 18) {
    verified: true;
  }
}

// exactOptionalPropertyTypes
interface UserDefaults {
  // The absence of a value represents 'system'
  colorThemeOverride?: "dark" | "light";
}
const settings: UserDefaults = {};
settings.colorThemeOverride = "dark";
settings.colorThemeOverride = "light";
// But not:
settings.colorThemeOverride = undefined;

// noFallthroughCasesInSwitch
const a: number = 6;
switch (a) {
  case 0:
    console.log("even");
  case 1:
    console.log("odd");
    break;
}

// noImplicitOverride
class Album {
  setup() {}
}
class MLAlbum extends Album {
  override setup() {}
}
class SharedAlbum extends Album {
  setup() {}
}

// noImplicitReturns
function lookupHeadphonesManufacturer(color: "blue" | "black"): string {
  if (color === "blue") {
    return "beats";
  } else {
    ("bose");
  }
}

// noPropertyAccessFromIndexSignature
interface GameSettings {
  // Known up-front properties
  speed: "fast" | "medium" | "slow";
  quality: "high" | "low";

  // Assume anything unknown to the interface
  // is a string.
  [key: string]: string;
}
const _settings: GameSettings = { speed: "fast", quality: "low" };
_settings.speed;
_settings.quality;
_settings.username;

// noUncheckedIndexedAccess
interface EnvironmentVars {
  NAME: string;
  OS: string;
  // 未知のプロパティは、次のようなインデックスシグネチャで扱うことができます。
  [propName: string]: string;
}
declare const env: EnvironmentVars;
env.NAME;
env.OS;
const x = env["NODE_ENV"];
console.log(x);
