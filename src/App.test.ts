import { mount } from "@vue/test-utils";

import App from "./App.vue";

test("renders the template heading", () => {
  const wrapper = mount(App);

  expect(wrapper.get("h1").text()).toBe("Application Template");
});
