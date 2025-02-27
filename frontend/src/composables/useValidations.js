export function getValidationRules() {
  const passwordValidationRules = [
    (val) => !!val || "Please enter a password",
    (val) => !(val.length <= 3) || "Please type more than 8 characters",
  ];

  const emailValidationRules = [
    (val) => !!val || "Email required!",
    // (val, rules) =>
    //   rules.email(val) || 'Please enter a valid email address',
  ];

  return {
    passwordValidationRules,
    emailValidationRules,
  };
}
