import logging
import zaza.model as model


def setup_ceph_proxy():
    raw_admin_keyring = model.run_on_leader("ceph-mon", 'cat /etc/ceph/ceph.client.admin.keyring')["Stdout"]
    admin_keyring = raw_admin_keyring.split(' = ')[-1].rstrip()
    fsid = model.run_on_leader("ceph-mon", "leader-get fsid")["Stdout"]
    cluster_ips = model.get_app_ips("ceph-mon")

    proxy_config = {
        'auth-supported': 'cephx',
        'admin-key': admin_keyring,
        'fsid': fsid,
        'monitor-hosts': ' '.join(cluster_ips)
    }

    logging.debug('Config: {}'.format(proxy_config))

    model.set_application_config("ceph-proxy", proxy_config)
