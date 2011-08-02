=========
Changelog
=========

0.2
---

* *(Backwards Incompatible)* Move specifying a non default serializer from
  ``api.resource.get(format="yaml")`` to ``api.resource(format="yaml").get()``
  
* Reworked the internal ``Resource`` api to not clobber any kwargs passed to it. This
  fixes a bug where you couldn't use ``format`` or ``url`` as the name for one of
  the url parameters.

0.1.3
-----

* Fix for Resource.post() not passing kwargs to Resource.get()

0.1.2
-----

* Initial public release of Slumber