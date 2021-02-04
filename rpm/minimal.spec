Name:          minimal
Summary:       Minimal proc_macro for sb2
Version:       0.1
Release:       1
License:       GPLv3
URL:           http://git.sailfishos.org/
Source0:       %{name}-%{version}.tgz
Source1:       cargo.tgz
BuildRequires: cargo rust-std-static-armv7-unknown-linux-gnueabihf

%description
%{summary}

%prep
%setup -q -n %{name}-%{version}
tar xzf %{SOURCE1}

cat <<EOF > $PWD/shenv
#!/bin/bash
export LD_PRELOAD=/usr/lib/libsb2/libsb2.so.1
exec /usr/bin/env "\$@"
EOF
chmod +x $PWD/shenv

# Test
$PWD/shenv pwd

%build
export SB2_RUST_TARGET_TRIPLE=armv7-unknown-linux-gnueabihf
export SB2_RUST_USE_REAL_FN=Yes
export SB2_RUST_EXECVP_SHIM="$PWD/shenv"
export SB2_RUST_USE_REAL_EXECVP=Yes

export CARGO_HOME=$PWD/.cargo
export CARGO_LOG=debug
cargo build -vv --target=armv7-unknown-linux-gnueabihf --offline

%install
rm -rf %{buildroot}
export SB2_RUST_TARGET_TRIPLE=armv7-unknown-linux-gnueabihf
export SB2_RUST_USE_REAL_FN=Yes
export SB2_RUST_EXECVP_SHIM="$PWD/shenv"
export SB2_RUST_USE_REAL_EXECVP=Yes
export CARGO_HOME=$PWD/.cargo
# https://github.com/rust-lang/cargo/issues/7688
cargo  -vv install --target=armv7-unknown-linux-gnueabihf --offline --root %{buildroot}/%{_prefix} --path .


%files
%defattr(-,root,root,-)
/
