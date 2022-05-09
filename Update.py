from Pools import Pools
from Pool import Pool
import Query
import Params
from util import *

def get_columns(pools : Pools, pool : Pool) -> list[str]:
    cur_share = pools.get_current_share(pool.gauge_ids)
    total_spend = Query.load_total_lp_spend()
    osmo_apr = 365 * cur_share * total_spend / pool.liquidity
    new_osmo_apr = 365 * pool.adjusted_share() * total_spend / pool.liquidity
    fee_apr = 365 * pool.fees_collected / pool.liquidity
    external_apr = 365 * pool.external_per_day / pool.liquidity
    based_assets = based(pool.assets)
    cur_total = osmo_apr + fee_apr + external_apr
    new_total = new_osmo_apr + fee_apr + external_apr
    return list(map(str, [
        pool.category,
        pool.pid,
        based_assets[0],
        based_assets[1],
        pool.liquidity,
        pool.fees_collected,
        pool.capped_fees(),
        pool.fee_share(),
        pool.external_per_day,
        pool.adjusted_revenue(),
        pool.adjusted_revenue_share(),
        pool.match_capped_share(),
        fee_apr,
        cur_share,
        osmo_apr,
        external_apr,
        pool.pid in Params.matched_pool_ids,
        pool.target_share(),
        pool.imbalance(),
        pool.maturity,
        pool.adjusted_share(),
        new_osmo_apr,
        cur_total,
        new_total,
        (new_total / cur_total) - 1
    ]))

def get_headers(pools: Pools) -> list[str]:
    return list(map(str, [
        "Category",
        "Pool ID"
        "Base Asset"
        "Pair Asset"
        "Liquidity",
        "Fees Collected",
        "Capped Fees",
        "Fee share",
        "External $ Per Day",
        "Adjusted Revenue",
        "Adjusted Revenue Share",
        "Match Capped Share",
        "Fee APR",
        "Current Share",
        "Current Osmo APR"
        "External APR",
        "Is Matched",
        "Target Share",
        "Imbalance",
        "Maturity",
        "Adjusted Share",
        "New Osmo APR",
        "Current Total APR",
        "New Total APR",
        "Effective APR Change",
    ]))

def get_totals(pools: Pools) -> list[str]:
    return list(map(str, [
        "",
        ""
        ""
        ""
        "Liquidity",
        "Fees Collected",
        "Capped Fees",
        "",
        "External $ Per Day",
        "Adjusted Revenue",
        "",
        "",
        "Fee APR",
        "Current Share",
        "Current Osmo APR"
        "External APR",
        "",
        "Target Share",
        "",
        "",
        "",
        "New Osmo APR",
        "Current Total APR",
        "New Total APR",
        "",
    ]))

def update() -> None:
    pools = Pools()
    lines = [",".join(get_headers(pools))] + [",".join(get_totals(pools))] + sorted([
        ",".join(get_columns(pools, pools.pools[pid]))
        for pid in sorted(pools.pools.keys())], key=lambda x: x[0])

    write_csv("data/incentives.csv", lines)

    write_csv("data/new_gauges.csv", [str(gid)+","+str(weight) for (gid,weight) in pools.new_gauges().items()])



if __name__ == "__main__":
    update()