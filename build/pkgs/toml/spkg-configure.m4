SAGE_SPKG_CONFIGURE([toml], [
    SAGE_PYTHON_PACKAGE_CHECK([toml])
  ], [dnl REQUIRED-CHECK
    AC_REQUIRE([SAGE_SPKG_CONFIGURE_TOX])
    dnl toml is only needed when we cannot use system tox.
    AS_VAR_SET([SPKG_REQUIRE], [$sage_spkg_install_tox])
  ])
