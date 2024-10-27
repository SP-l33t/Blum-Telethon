(async function () {
// dumps/game-Bg7iVTVS.js
  var v = globalThis || undefined || self;
  var _;
  var g = new Array(128).fill(undefined);
  g.push(undefined, null, true, false);

  function c(e) {
    return g[e];
  }

  var m = g.length;

  function M(e) {
    e < 132 || (g[e] = m, m = e);
  }

  function w(e) {
    const n = c(e);
    return M(e), n;
  }

  var d = 0;
  var p = null;

  function S() {
    return (p === null || p.byteLength === 0) && (p = new Uint8Array(_.memory.buffer)), p;
  }

  var O = typeof TextEncoder < "u" ? new TextEncoder("utf-8") : {
    encode: () => {
      throw Error("TextEncoder not available");
    }
  };
  var W = typeof O.encodeInto == "function" ? function (e, n) {
    return O.encodeInto(e, n);
  } : function (e, n) {
    const t = O.encode(e);
    return n.set(t), {read: e.length, written: t.length};
  };

  function h(e, n, t) {
    if (t === undefined) {
      const a = O.encode(e), y = n(a.length, 1) >>> 0;
      return S().subarray(y, y + a.length).set(a), d = a.length, y;
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
      const a = S().subarray(o + s, o + r), y = W(e, a);
      s += y.written, o = t(o, r, s, 1) >>> 0;
    }
    return d = s, o;
  }

  function I(e) {
    return e == null;
  }

  var l = null;

  function u() {
    return (l === null || l.buffer.detached === true || l.buffer.detached === undefined && l.buffer !== _.memory.buffer) && (l = new DataView(_.memory.buffer)), l;
  }

  function i(e) {
    m === g.length && g.push(g.length + 1);
    const n = m;
    return m = g[n], g[n] = e, n;
  }

  var E = typeof TextDecoder < "u" ? new TextDecoder("utf-8", {ignoreBOM: true, fatal: true}) : {
    decode: () => {
      throw Error("TextDecoder not available");
    }
  };
  typeof TextDecoder < "u" && E.decode();

  function A(e, n) {
    return e = e >>> 0, E.decode(S().subarray(e, e + n));
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

  function F(e) {
    try {
      const o = _.__wbindgen_add_to_stack_pointer(-16), f = h(e, _.__wbindgen_malloc, _.__wbindgen_realloc), s = d;
      _.proof(o, f, s);
      var n = u().getInt32(o + 4 * 0, true), t = u().getInt32(o + 4 * 1, true), r = u().getInt32(o + 4 * 2, true);
      if (r)
        throw w(t);
      return w(n);
    } finally {
      _.__wbindgen_add_to_stack_pointer(16);
    }
  }

  function B(e, n, t) {
    let r, o;
    try {
      const j = _.__wbindgen_add_to_stack_pointer(-16), q = h(e, _.__wbindgen_malloc, _.__wbindgen_realloc), N = d;
      _.pack(j, q, N, i(n), i(t));
      var f = u().getInt32(j + 4 * 0, true), s = u().getInt32(j + 4 * 1, true), a = u().getInt32(j + 4 * 2, true),
          y = u().getInt32(j + 4 * 3, true), k = f, U = s;
      if (y)
        throw k = 0, U = 0, w(a);
      return r = k, o = U, A(k, U);
    } finally {
      _.__wbindgen_add_to_stack_pointer(16), _.__wbindgen_free(r, o, 1);
    }
  }

  function b(e, n) {
    try {
      return e.apply(this, n);
    } catch (t) {
      _.__wbindgen_exn_store(i(t));
    }
  }

  async function D(e, n) {
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
      return t instanceof WebAssembly.Instance ? {instance: t, module: e} : t;
    }
  }

  function $() {
    const e = {};
    return e.wbg = {}, e.wbg.__wbindgen_object_drop_ref = function (n) {
      w(n);
    }, e.wbg.__wbindgen_string_get = function (n, t) {
      const r = c(t), o = typeof r == "string" ? r : undefined;
      var f = I(o) ? 0 : h(o, _.__wbindgen_malloc, _.__wbindgen_realloc), s = d;
      u().setInt32(n + 4 * 1, s, true), u().setInt32(n + 4 * 0, f, true);
    }, e.wbg.__wbindgen_is_object = function (n) {
      const t = c(n);
      return typeof t == "object" && t !== null;
    }, e.wbg.__wbindgen_is_undefined = function (n) {
      return c(n) === undefined;
    }, e.wbg.__wbindgen_in = function (n, t) {
      return c(n) in c(t);
    }, e.wbg.__wbindgen_is_bigint = function (n) {
      return typeof c(n) == "bigint";
    }, e.wbg.__wbindgen_bigint_from_u64 = function (n) {
      const t = BigInt.asUintN(64, n);
      return i(t);
    }, e.wbg.__wbindgen_jsval_eq = function (n, t) {
      return c(n) === c(t);
    }, e.wbg.__wbindgen_error_new = function (n, t) {
      const r = new Error(A(n, t));
      return i(r);
    }, e.wbg.__wbg_crypto_1d1f22824a6a080c = function (n) {
      const t = c(n).crypto;
      return i(t);
    }, e.wbg.__wbg_process_4a72847cc503995b = function (n) {
      const t = c(n).process;
      return i(t);
    }, e.wbg.__wbg_versions_f686565e586dd935 = function (n) {
      const t = c(n).versions;
      return i(t);
    }, e.wbg.__wbg_node_104a2ff8d6ea03a2 = function (n) {
      const t = c(n).node;
      return i(t);
    }, e.wbg.__wbindgen_is_string = function (n) {
      return typeof c(n) == "string";
    }, e.wbg.__wbg_require_cca90b1a94a0255b = function () {
      return b(function () {
        const n = module_game_Bg7iVTVS.require;
        return i(n);
      }, arguments);
    }, e.wbg.__wbindgen_is_function = function (n) {
      return typeof c(n) == "function";
    }, e.wbg.__wbindgen_string_new = function (n, t) {
      const r = A(n, t);
      return i(r);
    }, e.wbg.__wbg_msCrypto_eb05e62b530a1508 = function (n) {
      const t = c(n).msCrypto;
      return i(t);
    }, e.wbg.__wbg_randomFillSync_5c9c955aa56b6049 = function () {
      return b(function (n, t) {
        c(n).randomFillSync(w(t));
      }, arguments);
    }, e.wbg.__wbg_getRandomValues_3aa56aa6edec874c = function () {
      return b(function (n, t) {
        c(n).getRandomValues(c(t));
      }, arguments);
    }, e.wbg.__wbindgen_jsval_loose_eq = function (n, t) {
      return c(n) == c(t);
    }, e.wbg.__wbindgen_boolean_get = function (n) {
      const t = c(n);
      return typeof t == "boolean" ? t ? 1 : 0 : 2;
    }, e.wbg.__wbindgen_number_get = function (n, t) {
      const r = c(t), o = typeof r == "number" ? r : undefined;
      u().setFloat64(n + 8 * 1, I(o) ? 0 : o, true), u().setInt32(n + 4 * 0, !I(o), true);
    }, e.wbg.__wbindgen_as_number = function (n) {
      return +c(n);
    }, e.wbg.__wbg_String_b9412f8799faab3e = function (n, t) {
      const r = String(c(t)), o = h(r, _.__wbindgen_malloc, _.__wbindgen_realloc), f = d;
      u().setInt32(n + 4 * 1, f, true), u().setInt32(n + 4 * 0, o, true);
    }, e.wbg.__wbindgen_number_new = function (n) {
      return i(n);
    }, e.wbg.__wbindgen_object_clone_ref = function (n) {
      const t = c(n);
      return i(t);
    }, e.wbg.__wbg_getwithrefkey_edc2c8960f0f1191 = function (n, t) {
      const r = c(n)[c(t)];
      return i(r);
    }, e.wbg.__wbg_set_f975102236d3c502 = function (n, t, r) {
      c(n)[w(t)] = w(r);
    }, e.wbg.__wbg_get_3baa728f9d58d3f6 = function (n, t) {
      const r = c(n)[t >>> 0];
      return i(r);
    }, e.wbg.__wbg_length_ae22078168b726f5 = function (n) {
      return c(n).length;
    }, e.wbg.__wbg_newnoargs_76313bd6ff35d0f2 = function (n, t) {
      const r = new Function(A(n, t));
      return i(r);
    }, e.wbg.__wbg_next_de3e9db4440638b2 = function (n) {
      const t = c(n).next;
      return i(t);
    }, e.wbg.__wbg_next_f9cb570345655b9a = function () {
      return b(function (n) {
        const t = c(n).next();
        return i(t);
      }, arguments);
    }, e.wbg.__wbg_done_bfda7aa8f252b39f = function (n) {
      return c(n).done;
    }, e.wbg.__wbg_value_6d39332ab4788d86 = function (n) {
      const t = c(n).value;
      return i(t);
    }, e.wbg.__wbg_iterator_888179a48810a9fe = function () {
      return i(Symbol.iterator);
    }, e.wbg.__wbg_get_224d16597dbbfd96 = function () {
      return b(function (n, t) {
        const r = Reflect.get(c(n), c(t));
        return i(r);
      }, arguments);
    }, e.wbg.__wbg_call_1084a111329e68ce = function () {
      return b(function (n, t) {
        const r = c(n).call(c(t));
        return i(r);
      }, arguments);
    }, e.wbg.__wbg_new_525245e2b9901204 = function () {
      const n = new Object;
      return i(n);
    }, e.wbg.__wbg_self_3093d5d1f7bcb682 = function () {
      return b(function () {
        const n = self.self;
        return i(n);
      }, arguments);
    }, e.wbg.__wbg_window_3bcfc4d31bc012f8 = function () {
      return b(function () {
        const n = window.window;
        return i(n);
      }, arguments);
    }, e.wbg.__wbg_globalThis_86b222e13bdf32ed = function () {
      return b(function () {
        const n = globalThis.globalThis;
        return i(n);
      }, arguments);
    }, e.wbg.__wbg_global_e5a3fe56f8be9485 = function () {
      return b(function () {
        const n = v.global;
        return i(n);
      }, arguments);
    }, e.wbg.__wbg_instanceof_ArrayBuffer_61dfc3198373c902 = function (n) {
      let t;
      try {
        t = c(n) instanceof ArrayBuffer;
      } catch {
        t = false;
      }
      return t;
    }, e.wbg.__wbg_call_89af060b4e1523f2 = function () {
      return b(function (n, t, r) {
        const o = c(n).call(c(t), c(r));
        return i(o);
      }, arguments);
    }, e.wbg.__wbg_isSafeInteger_7f1ed56200d90674 = function (n) {
      return Number.isSafeInteger(c(n));
    }, e.wbg.__wbg_entries_7a0e06255456ebcd = function (n) {
      const t = Object.entries(c(n));
      return i(t);
    }, e.wbg.__wbg_buffer_b7b08af79b0b0974 = function (n) {
      const t = c(n).buffer;
      return i(t);
    }, e.wbg.__wbg_newwithbyteoffsetandlength_8a2cb9ca96b27ec9 = function (n, t, r) {
      const o = new Uint8Array(c(n), t >>> 0, r >>> 0);
      return i(o);
    }, e.wbg.__wbg_new_ea1883e1e5e86686 = function (n) {
      const t = new Uint8Array(c(n));
      return i(t);
    }, e.wbg.__wbg_set_d1e79e2388520f18 = function (n, t, r) {
      c(n).set(c(t), r >>> 0);
    }, e.wbg.__wbg_length_8339fcf5d8ecd12e = function (n) {
      return c(n).length;
    }, e.wbg.__wbg_instanceof_Uint8Array_247a91427532499e = function (n) {
      let t;
      try {
        t = c(n) instanceof Uint8Array;
      } catch {
        t = false;
      }
      return t;
    }, e.wbg.__wbg_newwithlength_ec548f448387c968 = function (n) {
      const t = new Uint8Array(n >>> 0);
      return i(t);
    }, e.wbg.__wbg_subarray_7c2e3576afe181d1 = function (n, t, r) {
      const o = c(n).subarray(t >>> 0, r >>> 0);
      return i(o);
    }, e.wbg.__wbindgen_bigint_get_as_i64 = function (n, t) {
      const r = c(t), o = typeof r == "bigint" ? r : undefined;
      u().setBigInt64(n + 8 * 1, I(o) ? BigInt(0) : o, true), u().setInt32(n + 4 * 0, !I(o), true);
    }, e.wbg.__wbindgen_debug_string = function (n, t) {
      const r = T(c(t)), o = h(r, _.__wbindgen_malloc, _.__wbindgen_realloc), f = d;
      u().setInt32(n + 4 * 1, f, true), u().setInt32(n + 4 * 0, o, true);
    }, e.wbg.__wbindgen_throw = function (n, t) {
      throw new Error(A(n, t));
    }, e.wbg.__wbindgen_memory = function () {
      const n = _.memory;
      return i(n);
    }, e;
  }

  function L(e, n) {
    return _ = e.exports, R.__wbindgen_wasm_module = n, l = null, p = null, _;
  }

  async function R(e) {
    if (_ !== undefined)
      return _;
    typeof e < "u" && Object.getPrototypeOf(e) === Object.prototype ? {module_or_path: e} = e : console.warn(), typeof e > "u" && (e = new URL("" + new URL("game_wasm_bg-BnV071fP.wasm", self.location.href).href, self.location.href));
    const n = $();
    (typeof e == "string" || typeof Request == "function" && e instanceof Request || typeof URL == "function" && e instanceof URL) && (e = fetch(e));
    const {instance: t, module: r} = await D(await e, n);
    return L(t, r);
  }

  var x;
  var V = async () => {
    x === undefined && (x = R()), await x;
  };
  async (e) => {
    await V();
    const {id: n, method: t, payload: r} = e.data;
    switch (t) {
      case "proof": {
        const o = F(r);
        return self.postMessage({id: n, ...o});
      }
      case "pack": {
        const o = B(r.gameId, r.challenge, r.earnedAssets);
        return self.postMessage({id: n, hash: o});
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
          var k = e.charCodeAt(l2 + o), P = r.charCodeAt(n + o);
          if (k !== P)
            break;
          k === 47 && (u2 = o);
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
  E2(m2, {default: () => q});
  A2(m2, y(h2()));
  var q = y(h2());

// index.ts
// import {readFileSync} from 'fs'
  const fs = await import('fs')
  var fl = fs.readFileSync(q.resolve("./game_wasm_bg-BnV071fP.wasm"));
  var uuid = () => "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, (ue) => {
    const Yi = Math.random() * 16 | 0;
    return (ue === "x" ? Yi : Yi & 3 | 8).toString(16);
  });

  async function generateChallenge(id) {
    await R(fl);
    const hash = F(id);
    return {id, ...hash};
  }

  async function generatePayload(id, gameId, challenge, earnedAssets) {
    const r = {
      id,
      gameId,
      challenge,
      earnedAssets
    };
    const hash = B(r.gameId, r.challenge, r.earnedAssets);
    return {payload: hash};
  }

  async function GetPayload(gid, points, dogs = 0) {
    const uuid1 = uuid();
    const challenge1 = await generateChallenge(gid);
    const r = {
      gameId: gid,
      challenge: {
        ...challenge1,
        id: uuid1
      },
      earnedAssets: {
        CLOVER: {
          amount: points.toString()
        },
        ...dogs > 0 && {DOGS: {amount: dogs.toString()}}
      }
    };
    const newPayload = await generatePayload(challenge1?.id, r.gameId, r.challenge, r.earnedAssets);
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
  var points = parseInt(args[1], 10);
  var dogs = args.length > 2 ? parseFloat(args[2]) : 0;
  if (isNaN(points)) {
    console.error("\u041D\u0435\u043A\u043E\u0440\u0440\u0435\u043A\u0442\u043D\u043E\u0435 \u0437\u043D\u0430\u0447\u0435\u043D\u0438\u0435 points. \u0414\u043E\u043B\u0436\u043D\u043E \u0431\u044B\u0442\u044C \u0446\u0435\u043B\u043E\u0435 \u0447\u0438\u0441\u043B\u043E.");
    process.exit(1);
  }
  var gx = await GetPayload(gid, points, dogs);

  console.log(gx);
})()