.. :changelog:

Changelog
=========


development version
-------------------

0.7.1
-----

* Correct support for UTF encoded responses.

0.6.2
-----

* Further Python 3 compatibility fixes, many thanks to Alexander Shchepetilnikov (irqed)

0.6.1
-----

* Remove ``simplejson`` dependency.

* Support range now Python 2.6 - Python 3.4


0.6.0
-----

* All HTTP methods support multipart/form-data.  The new ``files``
  parameter is directly passed to ``requests``.  Thanks to Philip
  Neustrom and Diego Gaustein.


0.5.2
-----

* Now compatible with ``requests`` 1.0 thanks to Matias Saguir.

* Fix bug when using default serializer.  Thanks to Andy McKay


0.4.2
-----

* Support decoded unicode url fragments - Thanks @collinwat


0.4.1
-----

* Added a ``session`` kwarg to ``slumber.API`` allowing passing a ``requests`` session
  that will be used instead of the slumber created one

0.4.0
-----

* *(Backwards Incompatible)* Switched from ``httplib2`` to ``requests``
* *(Backwards Incompatible)* Removed the Meta class Magic
* *(Backwards Incompatible)* Removed the ability to subclass ``slumber.API`` to specify defaults
* *(Backwards Incompatible)* New Syntax for Specifying Authentication

0.3.1
-----

* Fix regression where pre 0.3 urls were assumed to end in slash, and 0.3.0 presumed to end in not slash.
  Urls are now assumed to end in a slash, and if you don't want this behavior you can disable it by the
  append_slash kwarg/Meta option (set to False to disable it).
* Fix regression caused by a mistyped variable name.

0.3.0
-----

* Allowed nesting resources infinitely to allow more complex api usage.
* Cleaned up the Meta class and allow subclassing ``slumber.API``
* *(Backwards Incompatible)* Cleaned up the exception names.
* *(Backwards Incompatible)* Renamed the ``slumber.API`` serialization kwarg from
  default_format to format to be more consistent
* Improved the documentation
* Added Some Tests (This could still be better)

0.2.5
-----

* Fixed https urls and the accidental force to port 80
* Fixed the assumption that all urls end in a trailing slash

0.2.4
-----

* Fixed Including of Changelog.rst

0.2.3
-----

* Updated the docs to include a section about url parameters

0.2
----

* *(Backwards Incompatible)* Move specifying a non default serializer from
  ``api.resource.get(format="yaml")`` to ``api.resource(format="yaml").get()``

* Reworked the internal ``Resource`` api to not clobber any kwargs passed to it. This
  fixes a bug where you couldn't use ``format`` or ``url`` as the name for one of
  the url parameters.

0.1.3
-----

* Fix for ``Resource.post()`` not passing kwargs to ``Resource.get()``

0.1.2
-----

* Initial public release of Slumber
