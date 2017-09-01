# -*- coding:utf-8 -*-
import importlib
import logging
import pkgutil


def get_reg_blueprint(path, skip_blueprints=[]):
    bls = []
    for loader, name, is_package in pkgutil.iter_modules([path]):
        if is_package and name not in skip_blueprints:
            try:
                package = loader.find_module(name).load_module(name)
                view_name = package.__name__ + '.view'
                #print view_name
                view_module = importlib.import_module(view_name)
                if hasattr(view_module, 'blueprint'):
                    logging.info('Load blueprint:%s' % name)
                    bls.append(view_module.blueprint)
            except Exception, e:
                logging.error("import %s modules error e=%s" % (name, e.message))
                pass
    return bls
