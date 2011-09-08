import unittest
import slumber


class MetaTestCase(unittest.TestCase):

    def test_init_kwargs_to_attributes(self):
        m = slumber.Meta(item1="test", item2=41, item3="example")

        self.assertEqual(m.item1, "test")
        self.assertEqual(m.item2, 41)
        self.assertEqual(m.item3, "example")


class MetaMixinTestCase(unittest.TestCase):

    def test_init_kwargs_to_meta(self):
        class MetaMixinTest(slumber.MetaMixin, object):
            class Meta:
                item1 = None
                item2 = None
                item3 = None

        mmt = MetaMixinTest(item1="test", item2=41, item3="example")

        self.assertTrue(hasattr(mmt, "_meta"))
        self.assertTrue(isinstance(mmt._meta, slumber.Meta))

        self.assertEqual(mmt._meta.item1, "test")
        self.assertEqual(mmt._meta.item2, 41)
        self.assertEqual(mmt._meta.item3, "example")

    def test_meta_to_meta_defaults(self):
        class MetaMixinTest(slumber.MetaMixin, object):
            class Meta:
                item1 = None
                item2 = None
                item3 = None

        mmt = MetaMixinTest()

        self.assertTrue(hasattr(mmt, "_meta"))
        self.assertTrue(isinstance(mmt._meta, slumber.Meta))

        self.assertEqual(mmt._meta.item1, None)
        self.assertEqual(mmt._meta.item2, None)
        self.assertEqual(mmt._meta.item3, None)

    def test_meta_to_meta_defaults_with_init_kwargs(self):
        class MetaMixinTest(slumber.MetaMixin, object):
            class Meta:
                item1 = None
                item2 = None
                item3 = None

        mmt = MetaMixinTest(item2=41)

        self.assertTrue(hasattr(mmt, "_meta"))
        self.assertTrue(isinstance(mmt._meta, slumber.Meta))

        self.assertEqual(mmt._meta.item1, None)
        self.assertEqual(mmt._meta.item2, 41)
        self.assertEqual(mmt._meta.item3, None)
