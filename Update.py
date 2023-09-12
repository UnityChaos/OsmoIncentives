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
    imbalanceskew = 1 - Params.Category_weights["STABLE_STABLE"] + pools.total_variable_use("STABLE_STABLE")
    cur_total = osmo_apr + fee_apr + external_apr
    new_total = new_osmo_apr + fee_apr + external_apr
    return list(map(str, [
        pool.pid,
        based_assets[0],
        based_assets[1],
        pool.liquidity,
        pool.fees_collected,
        fee_apr,
        pool.external_per_day,
        external_apr,
        pool.ismatched,
        cur_share,
        osmo_apr,
        cur_share * Query.daily_osmo_issuance * Query.lp_mint_proportion,
        cur_share * Query.daily_osmo_issuance * Query.lp_mint_proportion * Query.OSMOPrice,
        cur_total
    ]))

def get_headers(pools: Pools) -> list[str]:
    return list(map(str, [
        "Pool ID",
        "Quote Asset",
        "Pair Asset",
        "Liquidity",
        "Spread Collected",
        "Swap APR",
        "External $ Per Day",
        "External APR",
        "Is Matched",
        "Current Share",
        "Current Osmo APR",
        "Daily OSMO Spend",
        "Dollar Equivalent Daily Spend",
        "Current Total APR"
    ]))

def get_totals(pools: Pools) -> list[str]:
    return list(map(str, [
        "",
        "",
        "",
        pools.total_liquidity(""),
        pools.total_fees(""),
        pools.avg_fee_apr(""),
        sum([p.external_per_day for p in pools.pools.values()]),
        "",
        "",
        "",
        "",
        Query.daily_osmo_issuance * Query.lp_mint_proportion,
        Query.daily_osmo_issuance * Query.lp_mint_proportion * Query.OSMOPrice,
        ""
    ]))

def update() -> None:
    pools = Pools()
    lines = [",".join(get_headers(pools))] + [",".join(get_totals(pools))] + [
        ",".join(get_columns(pools, p))
        for p in sorted(pools.pools.values(), reverse=True, key=lambda x: x.liquidity)]

    write_csv("data/incentives.csv", lines)

    write_csv("data/new_gauges.csv", [str(gid)+","+str(weight) for (gid,weight) in pools.new_gauges().items()])



if __name__ == "__main__":
    update()
