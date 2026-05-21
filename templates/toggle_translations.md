<%*
const snippet = "pali-translation-toggle";
const css = app.customCss;
const isEnabled = css.enabledSnippets.has(snippet);
if (isEnabled) {
    css.enabledSnippets.delete(snippet);
} else {
    css.enabledSnippets.add(snippet);
}
css.requestLoadSnippets();
-%>
