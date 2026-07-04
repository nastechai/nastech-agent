const CANONICAL_PACKAGE_NAME = "nastech-agentx";
const ALIAS_PACKAGE_NAME = "nastechagentx";

function getRelatedPackageNames(packageName) {
  if (packageName === CANONICAL_PACKAGE_NAME) {
    return [ALIAS_PACKAGE_NAME];
  }

  if (packageName === ALIAS_PACKAGE_NAME) {
    return [CANONICAL_PACKAGE_NAME];
  }

  return [];
}

function getAliasPackageName(packageName) {
  return packageName === CANONICAL_PACKAGE_NAME ? ALIAS_PACKAGE_NAME : packageName;
}

function getPackageBinNames(packageName) {
  const names = ["nastech", "nastech-agent"];

  if (packageName === ALIAS_PACKAGE_NAME) {
    names.push(ALIAS_PACKAGE_NAME);
  }

  return names;
}

module.exports = {
  ALIAS_PACKAGE_NAME,
  CANONICAL_PACKAGE_NAME,
  getAliasPackageName,
  getPackageBinNames,
  getRelatedPackageNames
};
