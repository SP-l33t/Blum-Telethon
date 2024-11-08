(async function () {
// dmp_new/game-BHQ4ZG5B.js
  var v = globalThis || undefined || self;
  var _;
  var g = new Array(128).fill(undefined);
  g.push(undefined, null, true, false);

  function i(e) {
    return g[e];
  }

  var w = 0;
  var m = null;

  function S() {
    return (m === null || m.byteLength === 0) && (m = new Uint8Array(_.memory.buffer)), m;
  }

  var O = typeof TextEncoder < "u" ? new TextEncoder("utf-8") : {
    encode: () => {
      throw Error("TextEncoder not available");
    }
  };
  var M = typeof O.encodeInto == "function" ? function (e, n) {
    return O.encodeInto(e, n);
  } : function (e, n) {
    const t = O.encode(e);
    return n.set(t), {
      read: e.length,
      written: t.length
    };
  };

  function p(e, n, t) {
    if (t === undefined) {
      const a = O.encode(e), y = n(a.length, 1) >>> 0;
      return S().subarray(y, y + a.length).set(a), w = a.length, y;
    }
    let r = e.length, o = n(r, 1) >>> 0;
    const f = S();
    let s = 0;
    for (; s < r; s++) {
      const a = e.charCodeAt(s);
      if (a > 127)
        break;
      f[o + s] = a;
    }
    if (s !== r) {
      s !== 0 && (e = e.slice(s)), o = t(o, r, r = s + e.length * 3, 1) >>> 0;
      const a = S().subarray(o + s, o + r), y = M(e, a);
      s += y.written, o = t(o, r, s, 1) >>> 0;
    }
    return w = s, o;
  }

  function h(e) {
    return e == null;
  }

  var d = null;

  function u() {
    return (d === null || d.buffer.detached === true || d.buffer.detached === undefined && d.buffer !== _.memory.buffer) && (d = new DataView(_.memory.buffer)), d;
  }

  var I = g.length;

  function W(e) {
    e < 132 || (g[e] = I, I = e);
  }

  function l(e) {
    const n = i(e);
    return W(e), n;
  }

  var E = typeof TextDecoder < "u" ? new TextDecoder("utf-8", {
    ignoreBOM: true,
    fatal: true
  }) : {
    decode: () => {
      throw Error("TextDecoder not available");
    }
  };
  typeof TextDecoder < "u" && E.decode();

  function A(e, n) {
    return e = e >>> 0, E.decode(S().subarray(e, e + n));
  }

  function c(e) {
    I === g.length && g.push(g.length + 1);
    const n = I;
    return I = g[n], g[n] = e, n;
  }

  function T(e) {
    const n = typeof e;
    if (n == "number" || n == "boolean" || e == null)
      return `${e}`;
    if (n == "string")
      return `"${e}"`;
    if (n == "symbol") {
      const o = e.description;
      return o == null ? "Symbol" : `Symbol(${o})`;
    }
    if (n == "function") {
      const o = e.name;
      return typeof o == "string" && o.length > 0 ? `Function(${o})` : "Function";
    }
    if (Array.isArray(e)) {
      const o = e.length;
      let f = "[";
      o > 0 && (f += T(e[0]));
      for (let s = 1; s < o; s++)
        f += ", " + T(e[s]);
      return f += "]", f;
    }
    const t = /\[object ([^\]]+)\]/.exec(toString.call(e));
    let r;
    if (t.length > 1)
      r = t[1];
    else
      return toString.call(e);
    if (r == "Object")
      try {
        return "Object(" + JSON.stringify(e) + ")";
      } catch {
        return "Object";
      }
    return e instanceof Error ? `${e.name}: ${e.message}
${e.stack}` : r;
  }

  function D(e) {
    try {
      const o = _.__wbindgen_add_to_stack_pointer(-16), f = p(e, _.__wbindgen_malloc, _.__wbindgen_realloc), s = w;
      _.proof(o, f, s);
      var n = u().getInt32(o + 4 * 0, true), t = u().getInt32(o + 4 * 1, true), r = u().getInt32(o + 4 * 2, true);
      if (r)
        throw l(t);
      return l(n);
    } finally {
      _.__wbindgen_add_to_stack_pointer(16);
    }
  }

  function F(e, n, t, r) {
    let o, f;
    try {
      const j = _.__wbindgen_add_to_stack_pointer(-16), N = p(e, _.__wbindgen_malloc, _.__wbindgen_realloc), V = w;
      _.pack(j, N, V, c(n), c(t), c(r));
      var s = u().getInt32(j + 4 * 0, true), a = u().getInt32(j + 4 * 1, true), y = u().getInt32(j + 4 * 2, true),
          C = u().getInt32(j + 4 * 3, true), x = s, U = a;
      if (C)
        throw x = 0, U = 0, l(y);
      return o = x, f = U, A(x, U);
    } finally {
      _.__wbindgen_add_to_stack_pointer(16), _.__wbindgen_free(o, f, 1);
    }
  }

  function b(e, n) {
    try {
      return e.apply(this, n);
    } catch (t) {
      _.__wbindgen_exn_store(c(t));
    }
  }

  async function $(e, n) {
    if (typeof Response == "function" && e instanceof Response) {
      if (typeof WebAssembly.instantiateStreaming == "function")
        try {
          return await WebAssembly.instantiateStreaming(e, n);
        } catch (r) {
          if (e.headers.get("Content-Type") != "application/wasm")
            console.warn("`WebAssembly.instantiateStreaming` failed because your server does not serve wasm with `application/wasm` MIME type. Falling back to `WebAssembly.instantiate` which is slower. Original error:\n", r);
          else
            throw r;
        }
      const t = await e.arrayBuffer();
      return await WebAssembly.instantiate(t, n);
    } else {
      const t = await WebAssembly.instantiate(e, n);
      return t instanceof WebAssembly.Instance ? {
        instance: t,
        module: e
      } : t;
    }
  }

  function B() {
    const e = {};
    return e.wbg = {}, e.wbg.__wbindgen_string_get = function (n, t) {
      const r = i(t), o = typeof r == "string" ? r : undefined;
      var f = h(o) ? 0 : p(o, _.__wbindgen_malloc, _.__wbindgen_realloc), s = w;
      u().setInt32(n + 4 * 1, s, true), u().setInt32(n + 4 * 0, f, true);
    }, e.wbg.__wbindgen_object_drop_ref = function (n) {
      l(n);
    }, e.wbg.__wbindgen_error_new = function (n, t) {
      const r = new Error(A(n, t));
      return c(r);
    }, e.wbg.__wbindgen_is_bigint = function (n) {
      return typeof i(n) == "bigint";
    }, e.wbg.__wbindgen_bigint_from_u64 = function (n) {
      const t = BigInt.asUintN(64, n);
      return c(t);
    }, e.wbg.__wbindgen_jsval_eq = function (n, t) {
      return i(n) === i(t);
    }, e.wbg.__wbindgen_is_object = function (n) {
      const t = i(n);
      return typeof t == "object" && t !== null;
    }, e.wbg.__wbindgen_is_undefined = function (n) {
      return i(n) === undefined;
    }, e.wbg.__wbindgen_in = function (n, t) {
      return i(n) in i(t);
    }, e.wbg.__wbg_crypto_1d1f22824a6a080c = function (n) {
      const t = i(n).crypto;
      return c(t);
    }, e.wbg.__wbg_process_4a72847cc503995b = function (n) {
      const t = i(n).process;
      return c(t);
    }, e.wbg.__wbg_versions_f686565e586dd935 = function (n) {
      const t = i(n).versions;
      return c(t);
    }, e.wbg.__wbg_node_104a2ff8d6ea03a2 = function (n) {
      const t = i(n).node;
      return c(t);
    }, e.wbg.__wbindgen_is_string = function (n) {
      return typeof i(n) == "string";
    }, e.wbg.__wbg_require_cca90b1a94a0255b = function () {
      return b(function () {
        const n = module_game_BHQ4ZG5B.require;
        return c(n);
      }, arguments);
    }, e.wbg.__wbindgen_is_function = function (n) {
      return typeof i(n) == "function";
    }, e.wbg.__wbindgen_string_new = function (n, t) {
      const r = A(n, t);
      return c(r);
    }, e.wbg.__wbg_msCrypto_eb05e62b530a1508 = function (n) {
      const t = i(n).msCrypto;
      return c(t);
    }, e.wbg.__wbg_randomFillSync_5c9c955aa56b6049 = function () {
      return b(function (n, t) {
        i(n).randomFillSync(l(t));
      }, arguments);
    }, e.wbg.__wbg_getRandomValues_3aa56aa6edec874c = function () {
      return b(function (n, t) {
        i(n).getRandomValues(i(t));
      }, arguments);
    }, e.wbg.__wbindgen_jsval_loose_eq = function (n, t) {
      return i(n) == i(t);
    }, e.wbg.__wbindgen_boolean_get = function (n) {
      const t = i(n);
      return typeof t == "boolean" ? t ? 1 : 0 : 2;
    }, e.wbg.__wbindgen_number_get = function (n, t) {
      const r = i(t), o = typeof r == "number" ? r : undefined;
      u().setFloat64(n + 8 * 1, h(o) ? 0 : o, true), u().setInt32(n + 4 * 0, !h(o), true);
    }, e.wbg.__wbindgen_as_number = function (n) {
      return +i(n);
    }, e.wbg.__wbindgen_number_new = function (n) {
      return c(n);
    }, e.wbg.__wbindgen_object_clone_ref = function (n) {
      const t = i(n);
      return c(t);
    }, e.wbg.__wbg_getwithrefkey_edc2c8960f0f1191 = function (n, t) {
      const r = i(n)[i(t)];
      return c(r);
    }, e.wbg.__wbg_set_f975102236d3c502 = function (n, t, r) {
      i(n)[l(t)] = l(r);
    }, e.wbg.__wbg_String_b9412f8799faab3e = function (n, t) {
      const r = String(i(t)), o = p(r, _.__wbindgen_malloc, _.__wbindgen_realloc), f = w;
      u().setInt32(n + 4 * 1, f, true), u().setInt32(n + 4 * 0, o, true);
    }, e.wbg.__wbg_get_3baa728f9d58d3f6 = function (n, t) {
      const r = i(n)[t >>> 0];
      return c(r);
    }, e.wbg.__wbg_length_ae22078168b726f5 = function (n) {
      return i(n).length;
    }, e.wbg.__wbg_newnoargs_76313bd6ff35d0f2 = function (n, t) {
      const r = new Function(A(n, t));
      return c(r);
    }, e.wbg.__wbg_next_de3e9db4440638b2 = function (n) {
      const t = i(n).next;
      return c(t);
    }, e.wbg.__wbg_next_f9cb570345655b9a = function () {
      return b(function (n) {
        const t = i(n).next();
        return c(t);
      }, arguments);
    }, e.wbg.__wbg_done_bfda7aa8f252b39f = function (n) {
      return i(n).done;
    }, e.wbg.__wbg_value_6d39332ab4788d86 = function (n) {
      const t = i(n).value;
      return c(t);
    }, e.wbg.__wbg_iterator_888179a48810a9fe = function () {
      return c(Symbol.iterator);
    }, e.wbg.__wbg_get_224d16597dbbfd96 = function () {
      return b(function (n, t) {
        const r = Reflect.get(i(n), i(t));
        return c(r);
      }, arguments);
    }, e.wbg.__wbg_call_1084a111329e68ce = function () {
      return b(function (n, t) {
        const r = i(n).call(i(t));
        return c(r);
      }, arguments);
    }, e.wbg.__wbg_new_525245e2b9901204 = function () {
      const n = new Object;
      return c(n);
    }, e.wbg.__wbg_self_3093d5d1f7bcb682 = function () {
      return b(function () {
        const n = self.self;
        return c(n);
      }, arguments);
    }, e.wbg.__wbg_window_3bcfc4d31bc012f8 = function () {
      return b(function () {
        const n = window.window;
        return c(n);
      }, arguments);
    }, e.wbg.__wbg_globalThis_86b222e13bdf32ed = function () {
      return b(function () {
        const n = globalThis.globalThis;
        return c(n);
      }, arguments);
    }, e.wbg.__wbg_global_e5a3fe56f8be9485 = function () {
      return b(function () {
        const n = v.global;
        return c(n);
      }, arguments);
    }, e.wbg.__wbg_instanceof_ArrayBuffer_61dfc3198373c902 = function (n) {
      let t;
      try {
        t = i(n) instanceof ArrayBuffer;
      } catch {
        t = false;
      }
      return t;
    }, e.wbg.__wbg_call_89af060b4e1523f2 = function () {
      return b(function (n, t, r) {
        const o = i(n).call(i(t), i(r));
        return c(o);
      }, arguments);
    }, e.wbg.__wbg_isSafeInteger_7f1ed56200d90674 = function (n) {
      return Number.isSafeInteger(i(n));
    }, e.wbg.__wbg_entries_7a0e06255456ebcd = function (n) {
      const t = Object.entries(i(n));
      return c(t);
    }, e.wbg.__wbg_buffer_b7b08af79b0b0974 = function (n) {
      const t = i(n).buffer;
      return c(t);
    }, e.wbg.__wbg_newwithbyteoffsetandlength_8a2cb9ca96b27ec9 = function (n, t, r) {
      const o = new Uint8Array(i(n), t >>> 0, r >>> 0);
      return c(o);
    }, e.wbg.__wbg_new_ea1883e1e5e86686 = function (n) {
      const t = new Uint8Array(i(n));
      return c(t);
    }, e.wbg.__wbg_set_d1e79e2388520f18 = function (n, t, r) {
      i(n).set(i(t), r >>> 0);
    }, e.wbg.__wbg_length_8339fcf5d8ecd12e = function (n) {
      return i(n).length;
    }, e.wbg.__wbg_instanceof_Uint8Array_247a91427532499e = function (n) {
      let t;
      try {
        t = i(n) instanceof Uint8Array;
      } catch {
        t = false;
      }
      return t;
    }, e.wbg.__wbg_newwithlength_ec548f448387c968 = function (n) {
      const t = new Uint8Array(n >>> 0);
      return c(t);
    }, e.wbg.__wbg_subarray_7c2e3576afe181d1 = function (n, t, r) {
      const o = i(n).subarray(t >>> 0, r >>> 0);
      return c(o);
    }, e.wbg.__wbindgen_bigint_get_as_i64 = function (n, t) {
      const r = i(t), o = typeof r == "bigint" ? r : undefined;
      u().setBigInt64(n + 8 * 1, h(o) ? BigInt(0) : o, true), u().setInt32(n + 4 * 0, !h(o), true);
    }, e.wbg.__wbindgen_debug_string = function (n, t) {
      const r = T(i(t)), o = p(r, _.__wbindgen_malloc, _.__wbindgen_realloc), f = w;
      u().setInt32(n + 4 * 1, f, true), u().setInt32(n + 4 * 0, o, true);
    }, e.wbg.__wbindgen_throw = function (n, t) {
      throw new Error(A(n, t));
    }, e.wbg.__wbindgen_memory = function () {
      const n = _.memory;
      return c(n);
    }, e;
  }

  function L(e, n) {
    return _ = e.exports, R.__wbindgen_wasm_module = n, d = null, m = null, _;
  }

  async function R(e) {
    if (_ !== undefined)
      return _;
    typeof e < "u" && Object.getPrototypeOf(e) === Object.prototype ? {module_or_path: e} = e : console.warn(""), typeof e > "u" && (e = new URL("" + new URL("game_wasm_bg-DYwJl-6R.wasm", self.location.href).href, self.location.href));
    const n = B();
    (typeof e == "string" || typeof Request == "function" && e instanceof Request || typeof URL == "function" && e instanceof URL) && (e = fetch(e));
    const {instance: t, module: r} = await $(await e, n);
    return L(t, r);
  }

  var k;
  var q = async () => {
    k === undefined && (k = R()), await k;
  };
  async (e) => {
    await q();
    const {id: n, method: t, payload: r} = e.data;
    switch (t) {
      case "proof": {
        const o = D(r);
        return self.postMessage({
          id: n,
          ...o
        });
      }
      case "pack": {
        const o = F(r.gameId, r.challenge, r.earnedPoints, r.assetClicks);
        return self.postMessage({
          id: n,
          hash: o
        });
      }
      default: {
        const o = t;
        throw err(`Unknown method: ${o}`);
      }
    }
  };

// node:path
  var L2 = Object.create;
  var b2 = Object.defineProperty;
  var z = Object.getOwnPropertyDescriptor;
  var D2 = Object.getOwnPropertyNames;
  var T2 = Object.getPrototypeOf;
  var R2 = Object.prototype.hasOwnProperty;
  var _2 = (f, e) => () => (e || f((e = {exports: {}}).exports, e), e.exports);
  var E2 = (f, e) => {
    for (var r in e)
      b2(f, r, {get: e[r], enumerable: true});
  };
  var C = (f, e, r, l2) => {
    if (e && typeof e == "object" || typeof e == "function")
      for (let i2 of D2(e))
        !R2.call(f, i2) && i2 !== r && b2(f, i2, {get: () => e[i2], enumerable: !(l2 = z(e, i2)) || l2.enumerable});
    return f;
  };
  var A2 = (f, e, r) => (C(f, e, "default"), r && C(r, e, "default"));
  var y = (f, e, r) => (r = f != null ? L2(T2(f)) : {}, C(e || !f || !f.__esModule ? b2(r, "default", {
    value: f,
    enumerable: true
  }) : r, f));
  var h2 = _2((F2, S2) => {
    function c2(f) {
      if (typeof f != "string")
        throw new TypeError("Path must be a string. Received " + JSON.stringify(f));
    }

    function w2(f, e) {
      for (var r = "", l2 = 0, i2 = -1, s = 0, n, t = 0; t <= f.length; ++t) {
        if (t < f.length)
          n = f.charCodeAt(t);
        else {
          if (n === 47)
            break;
          n = 47;
        }
        if (n === 47) {
          if (!(i2 === t - 1 || s === 1))
            if (i2 !== t - 1 && s === 2) {
              if (r.length < 2 || l2 !== 2 || r.charCodeAt(r.length - 1) !== 46 || r.charCodeAt(r.length - 2) !== 46) {
                if (r.length > 2) {
                  var a = r.lastIndexOf("/");
                  if (a !== r.length - 1) {
                    a === -1 ? (r = "", l2 = 0) : (r = r.slice(0, a), l2 = r.length - 1 - r.lastIndexOf("/")), i2 = t, s = 0;
                    continue;
                  }
                } else if (r.length === 2 || r.length === 1) {
                  r = "", l2 = 0, i2 = t, s = 0;
                  continue;
                }
              }
              e && (r.length > 0 ? r += "/.." : r = "..", l2 = 2);
            } else
              r.length > 0 ? r += "/" + f.slice(i2 + 1, t) : r = f.slice(i2 + 1, t), l2 = t - i2 - 1;
          i2 = t, s = 0;
        } else
          n === 46 && s !== -1 ? ++s : s = -1;
      }
      return r;
    }

    function J(f, e) {
      var r = e.dir || e.root, l2 = e.base || (e.name || "") + (e.ext || "");
      return r ? r === e.root ? r + l2 : r + f + l2 : l2;
    }

    var g2 = {
      resolve: function () {
        for (var e = "", r = false, l2, i2 = arguments.length - 1; i2 >= -1 && !r; i2--) {
          var s;
          i2 >= 0 ? s = arguments[i2] : (l2 === undefined && (l2 = process.cwd()), s = l2), c2(s), s.length !== 0 && (e = s + "/" + e, r = s.charCodeAt(0) === 47);
        }
        return e = w2(e, !r), r ? e.length > 0 ? "/" + e : "/" : e.length > 0 ? e : ".";
      }, normalize: function (e) {
        if (c2(e), e.length === 0)
          return ".";
        var r = e.charCodeAt(0) === 47, l2 = e.charCodeAt(e.length - 1) === 47;
        return e = w2(e, !r), e.length === 0 && !r && (e = "."), e.length > 0 && l2 && (e += "/"), r ? "/" + e : e;
      }, isAbsolute: function (e) {
        return c2(e), e.length > 0 && e.charCodeAt(0) === 47;
      }, join: function () {
        if (arguments.length === 0)
          return ".";
        for (var e, r = 0; r < arguments.length; ++r) {
          var l2 = arguments[r];
          c2(l2), l2.length > 0 && (e === undefined ? e = l2 : e += "/" + l2);
        }
        return e === undefined ? "." : g2.normalize(e);
      }, relative: function (e, r) {
        if (c2(e), c2(r), e === r || (e = g2.resolve(e), r = g2.resolve(r), e === r))
          return "";
        for (var l2 = 1; l2 < e.length && e.charCodeAt(l2) === 47; ++l2)
          ;
        for (var i2 = e.length, s = i2 - l2, n = 1; n < r.length && r.charCodeAt(n) === 47; ++n)
          ;
        for (var t = r.length, a = t - n, v2 = s < a ? s : a, u2 = -1, o = 0; o <= v2; ++o) {
          if (o === v2) {
            if (a > v2) {
              if (r.charCodeAt(n + o) === 47)
                return r.slice(n + o + 1);
              if (o === 0)
                return r.slice(n + o);
            } else
              s > v2 && (e.charCodeAt(l2 + o) === 47 ? u2 = o : o === 0 && (u2 = 0));
            break;
          }
          var k2 = e.charCodeAt(l2 + o), P = r.charCodeAt(n + o);
          if (k2 !== P)
            break;
          k2 === 47 && (u2 = o);
        }
        var d2 = "";
        for (o = l2 + u2 + 1; o <= i2; ++o)
          (o === i2 || e.charCodeAt(o) === 47) && (d2.length === 0 ? d2 += ".." : d2 += "/..");
        return d2.length > 0 ? d2 + r.slice(n + u2) : (n += u2, r.charCodeAt(n) === 47 && ++n, r.slice(n));
      }, _makeLong: function (e) {
        return e;
      }, dirname: function (e) {
        if (c2(e), e.length === 0)
          return ".";
        for (var r = e.charCodeAt(0), l2 = r === 47, i2 = -1, s = true, n = e.length - 1; n >= 1; --n)
          if (r = e.charCodeAt(n), r === 47) {
            if (!s) {
              i2 = n;
              break;
            }
          } else
            s = false;
        return i2 === -1 ? l2 ? "/" : "." : l2 && i2 === 1 ? "//" : e.slice(0, i2);
      }, basename: function (e, r) {
        if (r !== undefined && typeof r != "string")
          throw new TypeError('"ext" argument must be a string');
        c2(e);
        var l2 = 0, i2 = -1, s = true, n;
        if (r !== undefined && r.length > 0 && r.length <= e.length) {
          if (r.length === e.length && r === e)
            return "";
          var t = r.length - 1, a = -1;
          for (n = e.length - 1; n >= 0; --n) {
            var v2 = e.charCodeAt(n);
            if (v2 === 47) {
              if (!s) {
                l2 = n + 1;
                break;
              }
            } else
              a === -1 && (s = false, a = n + 1), t >= 0 && (v2 === r.charCodeAt(t) ? --t === -1 && (i2 = n) : (t = -1, i2 = a));
          }
          return l2 === i2 ? i2 = a : i2 === -1 && (i2 = e.length), e.slice(l2, i2);
        } else {
          for (n = e.length - 1; n >= 0; --n)
            if (e.charCodeAt(n) === 47) {
              if (!s) {
                l2 = n + 1;
                break;
              }
            } else
              i2 === -1 && (s = false, i2 = n + 1);
          return i2 === -1 ? "" : e.slice(l2, i2);
        }
      }, extname: function (e) {
        c2(e);
        for (var r = -1, l2 = 0, i2 = -1, s = true, n = 0, t = e.length - 1; t >= 0; --t) {
          var a = e.charCodeAt(t);
          if (a === 47) {
            if (!s) {
              l2 = t + 1;
              break;
            }
            continue;
          }
          i2 === -1 && (s = false, i2 = t + 1), a === 46 ? r === -1 ? r = t : n !== 1 && (n = 1) : r !== -1 && (n = -1);
        }
        return r === -1 || i2 === -1 || n === 0 || n === 1 && r === i2 - 1 && r === l2 + 1 ? "" : e.slice(r, i2);
      }, format: function (e) {
        if (e === null || typeof e != "object")
          throw new TypeError('The "pathObject" argument must be of type Object. Received type ' + typeof e);
        return J("/", e);
      }, parse: function (e) {
        c2(e);
        var r = {root: "", dir: "", base: "", ext: "", name: ""};
        if (e.length === 0)
          return r;
        var l2 = e.charCodeAt(0), i2 = l2 === 47, s;
        i2 ? (r.root = "/", s = 1) : s = 0;
        for (var n = -1, t = 0, a = -1, v2 = true, u2 = e.length - 1, o = 0; u2 >= s; --u2) {
          if (l2 = e.charCodeAt(u2), l2 === 47) {
            if (!v2) {
              t = u2 + 1;
              break;
            }
            continue;
          }
          a === -1 && (v2 = false, a = u2 + 1), l2 === 46 ? n === -1 ? n = u2 : o !== 1 && (o = 1) : n !== -1 && (o = -1);
        }
        return n === -1 || a === -1 || o === 0 || o === 1 && n === a - 1 && n === t + 1 ? a !== -1 && (t === 0 && i2 ? r.base = r.name = e.slice(1, a) : r.base = r.name = e.slice(t, a)) : (t === 0 && i2 ? (r.name = e.slice(1, n), r.base = e.slice(1, a)) : (r.name = e.slice(t, n), r.base = e.slice(t, a)), r.ext = e.slice(n, a)), t > 0 ? r.dir = e.slice(0, t - 1) : i2 && (r.dir = "/"), r;
      }, sep: "/", delimiter: ":", win32: null, posix: null
    };
    g2.posix = g2;
    S2.exports = g2;
  });
  var m2 = {};
  E2(m2, {default: () => q2});
  A2(m2, y(h2()));
  var q2 = y(h2());

// index_new.ts
  const fs = await import('fs')
  var fl = fs.readFileSync(q2.resolve("./game_wasm_bg-DYwJl-6R.wasm"));
  var uuid = () => "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, (ue) => {
    const Yi = Math.random() * 16 | 0;
    return (ue === "x" ? Yi : Yi & 3 | 8).toString(16);
  });

  async function generateChallenge(id) {
    await R(fl);
    const hash = D(id);
    return {id, ...hash};
  }

  async function generatePayload(id, gameId, challenge, earnedPoints, assetClicks) {
    const r = {
      id,
      gameId,
      challenge,
      earnedPoints,
      assetClicks
    };
    const hash = F(r.gameId, r.challenge, r.earnedPoints, r.assetClicks);
    return {payload: hash};
  }

  async function GetPayload(gid, clover, freeze = 0, dogs = 0) {
    const uuid1 = uuid();
    const challenge = await generateChallenge(gid);
    const r = {
      gameId: gid,
      challenge: {
        ...challenge,
        id: uuid1
      },
      earnedPoints: {
        BP: {amount: clover}
      },
      assetClicks: {
        CLOVER: {clicks: clover},
        FREEZE: {clicks: freeze},
        BOMB: {clicks: 0}
      }
    };
    const newPayload = await generatePayload(challenge?.id, r.gameId, r.challenge, r.earnedPoints, r.assetClicks);
    return JSON.stringify({
      payload: newPayload?.payload,
      ...r
    });
  }

  var args = process.argv.slice(2);
  if (args.length < 2) {
    console.error("\u041D\u0435\u043E\u0431\u0445\u043E\u0434\u0438\u043C\u043E \u0443\u043A\u0430\u0437\u0430\u0442\u044C gid \u0438 points \u0432 \u043A\u0430\u0447\u0435\u0441\u0442\u0432\u0435 \u0430\u0440\u0433\u0443\u043C\u0435\u043D\u0442\u043E\u0432.");
    process.exit(1);
  }
  var gid = args[0];
  var clover = parseInt(args[1], 10);
  var freeze = args.length > 2 ? parseInt(args[2], 10) : 0;
  var dogs = args.length > 3 ? parseFloat(args[3]) : 0;
  if (isNaN(clover)) {
    console.error("\u041D\u0435\u043A\u043E\u0440\u0440\u0435\u043A\u0442\u043D\u043E\u0435 \u0437\u043D\u0430\u0447\u0435\u043D\u0438\u0435 points. \u0414\u043E\u043B\u0436\u043D\u043E \u0431\u044B\u0442\u044C \u0446\u0435\u043B\u043E\u0435 \u0447\u0438\u0441\u043B\u043E.");
    process.exit(1);
  }
  var gx = await GetPayload(gid, clover, freeze, dogs);
  console.log(gx);
})()
