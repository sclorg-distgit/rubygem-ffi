%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

%global gem_name ffi

Name:           %{?scl_prefix}rubygem-%{gem_name}
Version:        1.9.10
Release:        4%{?dist}
Summary:        FFI Extensions for Ruby
Group:          Development/Languages

License:        BSD
URL:            http://wiki.github.com/ffi/ffi
Source0:        http://rubygems.org/gems/%{gem_name}-%{version}.gem

Requires:       %{?scl_prefix_ruby}ruby(release)
Requires:       %{?scl_prefix_ruby}ruby(rubygems)
BuildRequires:  %{?scl_prefix_ruby}ruby-devel
BuildRequires:  %{?scl_prefix_ruby}rubygems-devel
BuildRequires:  libffi-devel
BuildRequires:  %{?scl_prefix}rubygem(rspec)
Requires:       %{?scl_prefix_ruby}ruby(rubygems)
Requires:       %{?scl_prefix_ruby}ruby(release)
Provides:       %{?scl_prefix}rubygem(%{gem_name}) = %{version}

# Explicitly require runtime subpackage, as long as older scl-utils do not generate it
Requires: %{?scl_prefix}runtime

%description
Ruby-FFI is a ruby extension for programmatically loading dynamic
libraries, binding functions within them, and calling those functions
from Ruby code. Moreover, a Ruby-FFI extension works without changes
on Ruby and JRuby. Discover why should you write your next extension
using Ruby-FFI here[http://wiki.github.com/ffi/ffi/why-use-ffi].

%package   doc
Summary:   Documentation for %{pkg_name}
Group:     Documentation
Requires:  %{?scl_prefix}%{pkg_name} = %{version}-%{release}

%description	doc
This package contains documentation for %{pkg_name}.

%prep
%{?scl:scl enable %{scl} - << \EOF}
gem unpack %{SOURCE0}
%{?scl:EOF}
%setup -q -D -T -n  %{gem_name}-%{version}

%{?scl:scl enable %{scl} - << \EOF}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec
%{?scl:EOF}

%build

# Create the gem as gem install only works on a gem file
%{?scl:scl enable %{scl} - << \EOF}
set -e
gem build %{gem_name}.gemspec
%gem_install
%{?scl:EOF}

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{gem_extdir_mri}
cp -a ./%{gem_extdir_mri}/* %{buildroot}%{gem_extdir_mri}/

pushd %{buildroot}
rm -f .%{gem_extdir_mri}/{gem_make.out,mkmf.log}
popd

# Remove the binary extension sources and build leftovers.
rm -rf %{buildroot}%{gem_instdir}/ext

%check
pushd .%{gem_instdir}
%{?scl:scl enable %{scl} - << \EOF}
make -f libtest/GNUmakefile \
	JFLAGS="%{optflags}"
%{?scl:EOF}

# test dies on arm, disabling on the arch
%{?scl:scl enable %{scl} - << \EOF}
ruby -Ilib:ext/ffi_c -S \
	rspec spec
%{?scl:EOF}

popd

%files
%doc %{gem_instdir}/COPYING
%doc %{gem_instdir}/README.md
%{gem_instdir}/LICENSE
%dir %{gem_instdir}

%exclude %{gem_instdir}/Rakefile
%exclude %{gem_instdir}/gen
%exclude %{gem_instdir}/libtest
%exclude %{gem_instdir}/ffi.gemspec

%{gem_libdir}
%{gem_extdir_mri}/
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%exclude %{gem_instdir}/spec

%changelog
* Thu Apr 07 2016 Pavel Valena <pvalena@redhat.com> - 1.9.10-4
- Add scl macros

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 08 2016 Vít Ondruch <vondruch@redhat.com> - 1.9.10-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.3

* Sat Oct  3 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.9.10-1
- 1.9.10

* Mon Jul 20 2015 Vít Ondruch <vondruch@redhat.com> - 1.9.3-7
- Fix dangling symlinks in -debuginfo package.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jan 23 2015 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 1.9.3-5
- fixed to build on aarch64

* Fri Jan 16 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.9.3-4
- Rebuild for ruby 2.2 again

* Thu Jan 15 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.9.3-3
- Rebuild for ruby 2.2
- Use rspec2 for now

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jun 05 2014 Dominic Cleal <dcleal@redhat.com> - 1.9.3-1
- Update to FFI 1.9.3

* Sat May  3 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.4.0-4
- F-21: rebuild for ruby 2.1 / rubygems 2.2

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar 26 2013 Vít Ondruch <vondruch@redhat.com> - 1.4.0-2
- Use %%{gem_extdir_mri} instead of %%{gem_extdir}.

* Wed Feb 20 2013 Vít Ondruch <vondruch@redhat.com> - 1.4.0-1
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0
- Update to FFI 1.4.0.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb 02 2012 Vít Ondruch <vondruch@redhat.com> - 1.0.9-4
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 14 2011 Bryan Kearney <bkearney@redhat.com> - 1.0.9-2
- Fixed the License, it is actually LGPL

* Mon Jun 13 2011 Bryan Kearney <bkearney@redhat.com> - 1.0.9-1
- Bring in 1.0.9 from upstream.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Mar 10 2010 Bryan Kearney <bkearney@redhat.com> - 0.6.2-1
- Power PC fixes from upstream which were found testing 0.6.2

* Tue Feb 22 2010 Bryan Kearney <bkearney@redhat.com> - 0.6.2-1
- Pull in 0.6.2 from upstream

* Tue Feb 22 2010 Bryan Kearney <bkearney@redhat.com> - 0.5.4-3
- Final updates based on package review

* Tue Feb 16 2010 Bryan Kearney <bkearney@redhat.com> - 0.5.4-2
- Updates Based on code review comments

* Mon Feb 15 2010 Bryan Kearney <bkearney@redhat.com> - 0.5.4-1
- Initial specfile
