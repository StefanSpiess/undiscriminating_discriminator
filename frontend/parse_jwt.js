(function (global) {
  function parseJwt(token) {
    try {
      const segments = token.split('.');
      if (segments.length !== 3) {
        return null;
      }
      const base64Url = segments[1];
      const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
      const jsonPayload = decodeURIComponent(
        atob(base64)
          .split('')
          .map(function (c) {
            return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
          })
          .join('')
      );
      return JSON.parse(jsonPayload);
    } catch (e) {
      return null;
    }
  }

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = parseJwt;
  } else {
    global.parseJwt = parseJwt;
  }
})(this);
